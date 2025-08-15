from enum import Enum
from pathlib import Path

from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool

crew_configs = Path(__file__).resolve().parent.parent / "config"


# class Provider(str, Enum):
#     STARHUB = "https://www.starhub.com/personal/broadband.html"
#     MYREPUBLIC = "https://myrepublic.net/sg/broadband/"

#     SINGTEL = "https://www.singtel.com/personal/products-services/broadband/fibre-broadband-plans"
#     WHIZCOMMS = "https://whizcomms.com.sg/promo/"

#     SIMBA = "https://www.simba.sg/broadband"
#     M1 = "https://www.m1.com.sg/home-broadband"

#     VIEWQUEST = "https://viewqwest.com/sg/residential/broadband/"


class ThirdParty(str, Enum):
    HARDWAREZONE = "https://forums.hardwarezone.com.sg/threads/official-readme-first-2025-sg-isp-comparison-latest-promo-deals.6665380/"


@CrewBase
class BroadbandCrew:
    agents_config = str(crew_configs / "agents.yaml")
    tasks_config = str(crew_configs / "tasks.yaml")

    @agent
    def thirdparty_scraper(self) -> Agent:
        return Agent(config=self.agents_config["thirdparty_scraper"], verbose=True)

    @agent
    def content_curator(self) -> Agent:
        return Agent(config=self.agents_config["content_curator"], verbose=True)

    # @agent
    # def rag_formatter(self) -> Agent:
    #     return Agent(config=self.agents_config["rag_formatter"], verbose=True)

    # Tasks
    @task
    def thirdparty_scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config["thirdparty_scrape_task"],
            agent=self.thirdparty_scraper(),
            tools=[ScrapeWebsiteTool(website_url=ThirdParty.HARDWAREZONE.value)],
        )

    @task
    def content_curator_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_curator_task"],
            agent=self.content_curator(),
            context=[self.thirdparty_scrape_task()],
        )

    # @task
    # def rag_formatter_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["rag_formatter_task"],
    #         agent=self.rag_formatter(),
    #         context=[self.content_curator_task()],
    #     )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.thirdparty_scraper(),
                self.content_curator(),
                # self.rag_formatter(),
            ],
            tasks=[
                self.thirdparty_scrape_task(),
                self.content_curator_task(),
                # self.rag_formatter_task(),
            ],
        )
