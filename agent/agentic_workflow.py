from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self, model_provider:str ="groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        self.tools = []
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()

        self.tools.extend([
            * self.weather_tools.weather_tool_list, 
            * self.place_search_tools.place_search_tool_list, 
            * self.calculator_tools.calculator_tool_list, 
            * self.currency_converter_tools.currency_converter_tool_list
            ])

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

        self.graph = None

        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        # based on this particular function only it is going to choose the appropriate tool
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}

# one LLM and multiple tools
# in langraph node=function (agent_function=Brain of my system=functionality=prompt=instruction only)
    def build_graph(self):
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition) # agent is passing the cursor to tools_condition and its trying to check whether I need to call the tool or stop the process
        graph_builder.add_edge("tools", "agent") # means it is workingin a loop, back and forth unless we get our final answer, once LLM satisfy then Final response this system is call ReAct system i.e reasoning and action
        # Reasoning=LLM | Action=Tool calling
        # multi-agent host these tools as separate-separate agents
        # input and out flowing in the form of state
        # state is list of messages, key message

        graph_builder.add_edge("agent", END)

        self.graph=graph_builder.compile()
        return self.graph


    def __call__(self):
        return self.build_graph()