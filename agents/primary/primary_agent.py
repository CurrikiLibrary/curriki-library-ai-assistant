import datetime
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from tools.library_explorer import LibraryExplorer

# The top-level assistant (aka agent) performs general Q&A and delegates specialized tasks to other agents.
# The task delegation is a simple form of semantic routing / does simple intent detection

# class PrimaryAgent which initializes llm instance using ChatBedrock
class PrimaryAgent:
    def __init__(self):
        self.llm = ChatBedrock(
            model_id="anthropic.claude-v2",
            model_kwargs={"temperature": 0.1},
        )
        self.primary_agent_tools = []
        library_explorer = LibraryExplorer()
        self.set_primary_agent_tools(library_explorer)

    def set_primary_agent_tools(self, tool):
        # push the tool to the primary agent tools
        self.primary_agent_tools.append(tool)

    def get_primary_agent_tools(self):
        return self.primary_agent_tools

    def runnable(self):
        # Call llm instance to create course
        # return self.llm.create_course(request, title, description, subject, grade_level, keywords)
        primary_agent_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful assistant (aka agent) for Curriki Library. "
                "Your primary role is to search for information and resources from the Curriki Library to answer the user queries."
                "If a user asks you to search or explore the Curriki Library, create a course, create a lesson, or create a quiz, "
                "delegate the work to the appropriate specialized agent by invoking the corresponding tool. "
                "Only the specialized agents are given permission to do this for the user. "
                "The user is not aware of the different specialized agents, so do not mention them; just quietly delegate through function calls. "
                "Provide detailed information to the user and answer their questions to the best of your ability. "
                "When searching, be persistent. Expand your query bounds if the first search returns no results. "
                "If a search comes up empty, expand your search before giving up."
                "\n\nCurrent user Query information:\n<Queries>\n{user_info}\n</Queries>"
                "\nCurrent time: {time}.",
            ),
            ("placeholder", "{messages}"),
        ]).partial(time=datetime.now())
        primary_agent_runnable = primary_agent_prompt | self.llm.bind_tools(self.primary_agent_tools)
        return primary_agent_runnable
    