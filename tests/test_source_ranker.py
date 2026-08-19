import sys
import os


sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


from src.agents.source_ranker import NewsSourceRanker



project_path=input(
    "请输入项目路径:"
).strip()



agent=NewsSourceRanker()



result=agent.run({

    "project_path":
        project_path

})


print(result)