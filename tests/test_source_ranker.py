import sys
import os


sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)


from src.agents.source_ranker import SourceRanker



project_path=input(
    "请输入项目路径:"
).strip()



agent=SourceRanker()



result=agent.run({

    "project_path":
        project_path

})


print(result)