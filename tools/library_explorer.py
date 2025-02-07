from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import boto3
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch
from opensearchpy import AWSV4SignerAuth
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from opensearchpy import RequestsHttpConnection

class LibraryExplorer:
    def __init__(self, library):
        self.library = library
        self.error = None
        self.chain = None
        load_dotenv()
        if os.getenv("AWS_OPENSEARCH_DOMAIN_ENDPOINT") is None:
            self.error = "Environment variables. not set to execute the Explore Library Tool."
        self.initializeRAG()
        

    def initializeRAG(self):
        aws_opensearch_url = os.getenv("AWS_OPENSEARCH_DOMAIN_ENDPOINT")
        credentials = boto3.Session().get_credentials()
        region = os.environ["AWS_REGION"]
        awsauth = AWSV4SignerAuth(credentials, region)
        bedrock_embeddings = BedrockEmbeddings(credentials_profile_name=os.environ["AWS_PROFILE"], region_name=region)
        vectorstore = OpenSearchVectorSearch(opensearch_url=aws_opensearch_url, 
            index_name='curriki-oer-library-index', 
            embedding_function=bedrock_embeddings,
            http_auth=awsauth,
            timeout=300,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

        metadata_field_info = [
            AttributeInfo(
                name="title",
                description="title of an open education resource",
                type="string",
            ),
            AttributeInfo(
                name="keywords",
                description="keywords are used to search an open education resource",
                type="string",
            ),
            AttributeInfo(
                name="educationlevels",
                description="education levels for which an open education resource is useful",
                type="string",
            ),
            AttributeInfo(
                name="subjectareas",
                description="subject areas an open education resource is related to",
                type="string",
            ),
            AttributeInfo(
                name="collections",
                description="collections in which an open education resource is organized",
                type="string",
            )
        ]
        
        document_content_description = "open education resource which is known as oer"
        llm = ChatBedrock(
            model_id="anthropic.claude-v2",
            model_kwargs={"temperature": 0.1},
        )
        query_retriever = SelfQueryRetriever.from_llm(
            llm=llm,
            vectorstore=vectorstore,
            metadata_field_info=metadata_field_info,
            document_contents=document_content_description,
            return_source_documents=True
        )
        qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        chain = create_retrieval_chain(
            retriever=query_retriever,
            combine_docs_chain=create_stuff_documents_chain(llm, prompt=qa_chat_prompt)
        )
        self.chain = chain

    @tool
    def explore(self, message):
        chain = self.chain
        response = chain.invoke({"input": message})
        answer = HumanMessage(content=response['answer']).content
        oer_references = []
        # iterate over the context
        for index, context in enumerate(response['context']):
            oer_title = context.metadata['title']
            oer_reference_text = f"Title: {oer_title}\n\nURL: {context.metadata['pageurl']}\n\nSource File: {context.metadata['source']}\n\nPage:{context.metadata['page']}\n\n"
            oer_reference_text += f"\n\nEducation Levels: {context.metadata['educationlevels']}\n\nSubject Areas: {context.metadata['subjectareas']}\n\nCollections: {context.metadata['collections']}"
            oer_reference_text += f"\n\nContent: \n{context.page_content}"
            # make dictionary of oer_title, oer_reference_text and index to append in oer_references
            oer_references.append({
                "name": f"{oer_title} ({index})",
                "content": oer_reference_text
            })
            
        oer_reference_names = [oer_reference["name"] for oer_reference in oer_references]
        if oer_reference_names:
            answer += f"\n\nSources: {', '.join(oer_reference_names)}"
        
        # return answer, oer_references as json
        return {"answer": answer, "oer_references": oer_references}
