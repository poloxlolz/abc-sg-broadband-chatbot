from crewai import Agent, Crew, Task
from crewai_tools import ScrapeWebsiteTool

tool_webscrape = ScrapeWebsiteTool(
    website_url="https://www.starhub.com/personal/broadband.html"
)


broadband_deal_hunter = Agent(
    role="Broadband",
    goal="Search for the best broadband deals",
    backstory="""You are an expert at searching broadband deals""",
    tools=[tool_webscrape],
    verbose=True,
)


task_research = Task(
    description="""\
    Find the best plan for the provided budget based on user input {budget}""",
    expected_output="""\
    The best broadband plan closest to my budget, present in a markdown file""",
    agent=broadband_deal_hunter,
)


crew = Crew(
    agents=[broadband_deal_hunter],
    tasks=[task_research],
    verbose=True,
)


budget = {
    "budget": "around $30 per month",
}


### this execution will take a few minutes to run


def get_deals():
    result = crew.kickoff(inputs=budget)
    return result.raw
