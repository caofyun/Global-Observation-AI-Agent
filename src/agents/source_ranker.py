import os
import json


from src.agents.base_agent import BaseAgent


# ==========================================
# 环球观察速递
# SourceRanker V2.0
#
# 新闻来源评级 Agent
#
# V2.0冻结实现：
#
# 输入：
# project_path/02_事实核验/verification.json
#
# 输出：
# project_path/03_来源评级/source_rank.json
#
# 职责：
# 新闻来源质量评级
#
# ==========================================


class SourceRanker(BaseAgent):


    # ======================================
    # 初始化
    # ======================================

    def __init__(self, project_path=None):

        super().__init__(
            "SourceRanker",
            project_path
        )

        self.source_database = (
            self.load_source_database()
        )


    # ======================================
    # 加载来源数据库
    # ======================================

    def load_source_database(self):

        config_path = os.path.join(

            "src",
            "config",
            "source_database.json"

        )


        if not os.path.exists(config_path):

            return {}


        try:

            with open(
                config_path,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)


        except Exception:

            return {}



    # ======================================
    # 来源名称标准化
    # ======================================

    def normalize_source(self, source):

        return str(
            source
        ).strip()



    # ======================================
    # 获取来源信息
    # ======================================

    def get_source_info(self, source):

        source = self.normalize_source(
            source
        )


        # 精确匹配

        if source in self.source_database:

            return self.source_database[source]


        # 模糊匹配

        for name, info in self.source_database.items():

            if name.lower() in source.lower():

                return info


        # 默认来源

        return {

            "level": "D",

            "score": 40,

            "type": "未知来源"

        }



    # ======================================
    # 来源去重
    # ======================================

    def analyze_sources(self, articles):


        source_map = {}


        for article in articles:


            source = self.normalize_source(

                article.get(
                    "source",
                    ""
                )

            )


            if not source:

                continue



            if source not in source_map:


                source_map[source] = {

                    "source_name": source,

                    "count": 1

                }


            else:


                source_map[source]["count"] += 1



        return list(
            source_map.values()
        )



    # ======================================
    # 计算验证评分
    #
    # 基于：
    # - 来源数量
    # - 交叉情况
    #
    # ======================================

    def calculate_verification_score(
        self,
        count
    ):


        if count >= 5:

            return 100


        elif count >= 3:

            return 85


        elif count >= 2:

            return 70


        else:

            return 50



    # ======================================
    # 来源等级转换
    # ======================================

    def convert_rank(
        self,
        credibility_score
    ):


        if credibility_score >= 85:

            return "HIGH"


        elif credibility_score >= 60:

            return "MEDIUM"


        else:

            return "LOW"



    # ======================================
    # 生成评级原因
    # ======================================

    def build_reason(
        self,
        source_info,
        verification_score
    ):


        reasons = []


        level = source_info.get(
            "level",
            "D"
        )


        if level in ["A", "B"]:

            reasons.append(
                "来源历史可信度较高"
            )


        else:

            reasons.append(
                "来源可信度有限"
            )


        if verification_score >= 70:

            reasons.append(
                "存在多来源交叉信息"
            )

        else:

            reasons.append(
                "交叉验证不足"
            )


        return "；".join(
            reasons
        )



    # ======================================
    # 执行Agent
    # ======================================

    def execute(
        self,
        input_data=None
    ):


        # ----------------------------------
        # 获取系统context
        # ----------------------------------

        project_path = self.project_path


        if not project_path:

            raise ValueError(
                "缺少project_path"
            )



        # ----------------------------------
        # 读取verification.json
        # ----------------------------------

        verification_path = os.path.join(

            project_path,

            "02_事实核验",

            "verification.json"

        )


        if not os.path.exists(
            verification_path
        ):

            raise FileNotFoundError(

                "未找到verification.json"

            )



        with open(

            verification_path,

            "r",

            encoding="utf-8"

        ) as f:

            verification_data = json.load(f)



        topic = verification_data.get(

            "topic",

            ""

        )


        articles = verification_data.get(

            "articles",

            []

        )


        sources_input = verification_data.get(

            "sources",

            []

        )



        # ----------------------------------
        # 来源分析
        # ----------------------------------

        article_sources = self.analyze_sources(

            articles

        )



        # 如果verification已有sources
        # 合并

        existing_sources = []


        for item in sources_input:

            if isinstance(item, dict):

                name = item.get(
                    "source",
                    ""
                )

            else:

                name = item


            if name:

                existing_sources.append({

                    "source_name":
                        self.normalize_source(name),

                    "count":
                        1

                })



        all_sources = article_sources + existing_sources



        # 去重

        merged = {}


        for item in all_sources:


            name = item["source_name"]


            if name not in merged:

                merged[name] = {

                    "source_name":
                        name,

                    "count":
                        item.get(
                            "count",
                            1
                        )

                }

            else:

                merged[name]["count"] += item.get(
                    "count",
                    1
                )



        source_results = []


        index = 1


        for item in merged.values():


            source_name = item["source_name"]


            info = self.get_source_info(

                source_name

            )


            credibility_score = info.get(

                "score",

                40

            )


            verification_score = self.calculate_verification_score(

                item["count"]

            )


            rank = self.convert_rank(

                credibility_score

            )


            source_results.append({

                "source_id":
                    f"source_{index}",


                "source_name":
                    source_name,


                "source_type":
                    info.get(
                        "type",
                        "未知"
                    ),


                "credibility_score":
                    credibility_score,


                "verification_score":
                    verification_score,


                "source_rank":
                    rank,


                "reason":
                    self.build_reason(
                        info,
                        verification_score
                    )

            })


            index += 1



        # ----------------------------------
        # 输出source_rank.json
        # ----------------------------------

        output_dir = os.path.join(

            project_path,

            "03_来源评级"

        )


        os.makedirs(

            output_dir,

            exist_ok=True

        )


        output_path = os.path.join(

            output_dir,

            "source_rank.json"

        )



        result = {

            "topic":

                topic,


            "sources":

                source_results

        }



        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                result,

                f,

                ensure_ascii=False,

                indent=4

            )



        print()
        print("==============================")
        print("SourceRanker V2.0完成")
        print("==============================")

        print(
            f"评级来源数量：{len(source_results)}"
        )

        print(
            "source_rank.json生成成功"
        )



        return result