import os
import json


from src.agents.base_agent import BaseAgent


# ==========================================
# 环球观察速递
# NewsSourceRanker V2.0
#
# 新闻来源评级Agent
#
# 功能：
#
# 1. 读取verification.json
# 2. 提取新闻来源
# 3. 来源去重
# 4. 读取来源数据库
# 5. 来源等级评级
# 6. 计算来源质量分
# 7. 判断来源结构
# 8. 输出风险提示
# 9. 生成source_rank.json
#
# ==========================================


class NewsSourceRanker(BaseAgent):


    # ======================================
    # 初始化
    # ======================================

    def __init__(self):

        super().__init__(
            "新闻来源评级Agent V2.0"
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


        if not os.path.exists(
            config_path
        ):

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
    # 标准化来源名称
    # ======================================

    def normalize_source(
        self,
        source
    ):


        return str(
            source
        ).strip()



    # ======================================
    # 获取来源评级
    # ======================================

    def get_source_info(
        self,
        source
    ):


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

            "level":"D",

            "score":40,

            "type":"未知来源"

        }



    # ======================================
    # 来源分析
    # ======================================

    def analyze_sources(
        self,
        results
    ):


        source_map = {}


        for item in results:


            source = self.normalize_source(

                item.get(
                    "source",
                    ""
                )

            )


            if not source:

                continue



            if source not in source_map:


                source_map[source] = {


                    "source":source,


                    "count":1

                }


            else:


                source_map[source]["count"] += 1



        return list(
            source_map.values()
        )



    # ======================================
    # 来源评分
    # ======================================

    def calculate_quality_score(
        self,
        source_details
    ):


        if not source_details:

            return 0



        total_score = 0


        level_count = {


            "A":0,

            "B":0,

            "C":0,

            "D":0

        }



        for item in source_details:


            info = item.get(
                "info",
                {}
            )


            score = info.get(

                "score",

                40

            )


            level = info.get(

                "level",

                "D"

            )


            level_count[level] += 1



            total_score += score



        # 平均来源质量

        average = (

            total_score /
            len(source_details)

        )



        # 独立来源奖励

        diversity_bonus = min(

            len(source_details) * 2,

            20

        )



        final_score = int(

            average * 0.8
            +
            diversity_bonus

        )



        return min(

            final_score,

            100

        )



    # ======================================
    # 综合等级
    # ======================================

    def get_quality_level(
        self,
        score
    ):


        if score >= 80:

            return "HIGH"


        elif score >= 60:

            return "MEDIUM"


        else:

            return "LOW"



    # ======================================
    # 风险分析
    # ======================================

    def generate_warnings(
        self,
        level_count
    ):


        warnings = []



        if level_count.get(
            "A",
            0
        ) == 0:


            warnings.append(

                "缺少A级权威来源确认"

            )



        if level_count.get(
            "D",
            0
        ) >= 5:


            warnings.append(

                "大量来源质量较低，需要进一步核验"

            )



        if (
            level_count.get("A",0)
            +
            level_count.get("B",0)
        ) < 2:


            warnings.append(

                "缺少多类型高质量来源交叉验证"

            )



        return warnings



    # ======================================
    # 执行Agent
    # ======================================

    def execute(
        self,
        input_data
    ):


        if isinstance(
            input_data,
            str
        ):


            verification_path = input_data


        else:


            verification_path = input_data.get(

                "verification_path"

            )



        if not verification_path:

            raise ValueError(

                "缺少verification_path"

            )



        with open(

            verification_path,

            "r",

            encoding="utf-8"

        ) as f:


            data = json.load(f)



        topic = data.get(

            "topic",

            ""

        )


        results = data.get(

            "results",

            []

        )



        print()

        print(
            "=============================="
        )

        print(
            "NewsSourceRanker V2.0"
        )

        print(
            "=============================="
        )



        # 来源去重

        unique_sources = self.analyze_sources(

            results

        )



        source_details = []



        level_count = {


            "A":0,

            "B":0,

            "C":0,

            "D":0

        }



        for item in unique_sources:


            info = self.get_source_info(

                item["source"]

            )


            level = info.get(

                "level",

                "D"

            )


            level_count[level] += 1



            source_details.append({


                "source":
                    item["source"],


                "count":
                    item["count"],


                "level":
                    level,


                "score":
                    info.get(
                        "score",
                        40
                    ),


                "type":
                    info.get(
                        "type",
                        "未知"
                    )


            })



        quality_score = (

            self.calculate_quality_score(

                [

                    {
                        "info":
                        self.get_source_info(
                            x["source"]
                        )

                    }

                    for x in unique_sources

                ]

            )

        )



        quality_level = (

            self.get_quality_level(

                quality_score

            )

        )



        warnings = self.generate_warnings(

            level_count

        )



        result = {


            "topic":

                topic,


            "total_sources":

                len(results),



            "unique_sources":

                len(unique_sources),



            "level_statistics":

                level_count,



            "quality_score":

                quality_score,



            "quality_level":

                quality_level,



            "sources":

                source_details,



            "warnings":

                warnings


        }



        # 保存文件

        project_path = os.path.dirname(

            os.path.dirname(

                verification_path

            )

        )


        output_path = os.path.join(

            project_path,

            "01_新闻资料",

            "source_rank.json"

        )


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

        print(
            "=============================="
        )

        print(
            "NewsSourceRanker V2.0完成"
        )

        print(
            "=============================="
        )


        print(

            f"独立来源:{len(unique_sources)}"

        )


        print(

            f"质量评分:{quality_score}"

        )


        print(

            f"综合等级:{quality_level}"

        )


        print()

        print(

            "source_rank.json生成成功"

        )


        return result