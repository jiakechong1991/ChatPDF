# -*- coding:utf-8 -*-
import cn2an
from openai import OpenAI
from config import llm_model, total_token
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8082/v1"



def api_llm(history_list):
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    chat_response = client.chat.completions.create(
        model=llm_model,
        messages=history_list,
        temperature=0.7,
        top_p=0.8,
        #stream=True,
        #stop=["<|im_end|>", "<|endoftext|>"], 
        max_tokens=10000,
        extra_body={
            "repetition_penalty": 1.05,
        },
    )

    print("本次token消耗: {a}".format(a=chat_response.usage.total_tokens))
    total_token["total"] += chat_response.usage.total_tokens
    total_token["in_num"] += chat_response.usage.prompt_tokens
    total_token["out_num"] += chat_response.usage.completion_tokens

    res = chat_response.choices[0].message.content
    return res

def  api_llm_stream(history_list):
    # print("=========history_list================")
    # print(history_list)
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    for chunk in client.chat.completions.create(
        model=llm_model,
        messages=history_list,
        temperature=0.7,
        top_p=0.8,
        stream=True,
        #stop=["<|im_end|>", "<|endoftext|>"], 
        max_tokens=10000,
        extra_body={
            "repetition_penalty": 1.05,
        },
    ):
        #chunk: ChatCompletionChunk(id='chat-1c4dc60f60be482b8586417fa56660ae', 
        # choices=[Choice(delta=ChoiceDelta(content='得到', function_call=None, refusal=None, role=None, 
        # tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1727287449, 
        # model='/home/wangxk/project/model_bin_common/Qwen2-7B-Instruct', object='chat.completion.chunk', 
        # service_tier=None, system_fingerprint=None, usage=None)
        if hasattr(chunk.choices[0].delta, "content"):
            chunk_str = ""
            if chunk.choices[0].delta.content:
                chunk_str = chunk.choices[0].delta.content 
            yield chunk_str




if __name__ == "__main__":
    pass
    history_list2 = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": """刘备为什么要攻打孙权呢？"""},
    ]
    history_list2 = [{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': '基于以下已知信息，简洁和专业的来回答用户的问题。用简体中文回答。\n\n已知内容:\n[1]\t "催督战船，到三江口。早见东吴船只，蔽江而来。为首一员大将，坐在船头上大呼曰：“吾乃甘宁也！谁敢来与我决战？”蔡瑁令弟蔡壎前进。两船将近，甘宁拈弓搭箭，望蔡壎射来，应弦而倒。宁驱船大进，万弩齐发。曹军不能抵当。右边蒋钦，左边韩当，直冲入曹军队中。曹军大半是青、徐之兵，素不习水战，大江面上，战船一摆，早立脚不住。甘宁等三路战船，纵横水面。周瑜又催船助战。曹军中箭着炮者，不计其数，从巳时直杀到未时。周瑜虽得利，只恐寡不敌众，遂下令鸣金，收住船只。\n曹军败回。操登旱寨，再整军士，唤蔡瑁、张允责之曰：“东吴兵少，反为所败，是汝等不用心耳！”蔡瑁曰：“荆州水军，久不操练；青、徐之军，又素不习水战。故尔致败。今当先立水寨，令青、徐军在中，荆州军在外，每日教习精熟，方可用之。”操曰：“汝既为水军都督，可以便宜从事，何必禀我！”于是张、蔡二人，自去训练水军。沿江一带分二十四座水门，以大船居于外为城郭，小船居于内，可通往来，至晚点上灯火，照得天心水面通红。旱寨三百余里，烟火不绝。\n却说周瑜得胜回寨，犒赏三军，一面差人到吴侯处报捷。当夜瑜登高观望，只见西边火光接天。左右告曰：“此皆北军灯火之光也。”瑜亦心惊。次日，瑜欲亲往探看曹军水寨，乃命收拾楼船一只，带着鼓东，随行健将数员，各带强弓硬弩，一齐上船迤逦前进。至操寨边，瑜命下了矴石，楼船上鼓乐齐奏。瑜暗窥他水寨，大惊曰：“此深得水军之妙也！”问：“水军都督是谁？”左右曰：“蔡瑁、涨允。”瑜思曰：“二人久居江东，谙习水战，吾必设计先除此二人，然后可以破曹。”正窥看间，早有"\n[2]\t "唤军中铁匠，连夜打造连环大钉，锁住船只。诸军闻之，俱各喜悦。后人有诗曰：“赤壁鏖兵用火攻，运筹决策尽皆同。若非庞统连环计，公瑾安能立大功？”\n庞统又谓操曰：“某观江左豪杰，多有怨周瑜者；某凭三寸舌，为丞相说之，使皆来降。周瑜孤立无援，必为丞相所擒。瑜既破，则刘备无所用矣。”操曰：“先生果能成大功，操请奏闻天子，封为三公之列。”统曰：“某非为富贵，但欲救万民耳。丞相渡江，慎勿杀害。”操曰：“吾替天行道，安忍杀戮人民！”统拜求榜文，以安宗族。操曰：“先生家属，现居何处？”统曰：“只在江边。若得此榜，可保全矣。”操命写榜佥押付统。统拜谢曰：“别后可速进兵，休待周郎知觉。”操然之。统拜别，至江边，正欲下船，忽见岸上一人，道袍竹冠，一把扯住统曰：“你好大胆！黄盖用苦肉计，阚泽下诈降书，你又来献连环计：只恐烧不尽绝！你们把出这等毒手来，只好瞒曹操，也须瞒我不得！”?得庞统魂飞魄散。正是：莫道东南能制胜，谁云西北独无人？毕竟此人是谁，且看下文分解。\n第四十八回 宴长江曹操赋诗 锁战船北军用武\n却说庞统闻言，吃了一惊，急回视其人，原来却是徐庶。统见是故人，心下方定。回顾左右无人，乃曰：“你若说破我计，可惜江南八十一州百姓，皆是你送了也！”庶笑曰：“此间八十三万人马，性命如何？”统曰：“元直真欲破我计耶？”庶曰：“吾感刘皇叔厚恩，未尝忘报。曹操送死吾母，吾已说过终身不设一谋，今安肯破兄良策？只是我亦随军在此，兵败之后，玉石不分，岂能免难？君当教我脱身之术，我即缄口远避矣。”统笑曰：“元直如此高见远识，谅此有何难哉！"\n[3]\t "城池？倘有差失，悔无及矣！妾昔在长安，已为将军所弃，幸赖庞舒私藏妾身，再得与将军相聚；孰知今又弃妾而去乎？将军前程万里，请勿以妾为念！”言罢痛哭。布闻言愁闷不决，入告貂蝉。貂蝉曰：“将军与妾作主，勿轻身自出。”布曰：“汝无忧虑。吾有画戟、赤兔马，谁敢近我！”乃出谓陈宫曰：“操军粮至者，诈也。操多诡计，吾未敢动。”宫出，叹曰：“吾等死无葬身之地矣！”布于是终日不出，只同严氏、貂蝉饮酒解闷。\n谋士许汜、王楷入见布，进计曰：今袁术在淮南，声势大振。将军旧曾与彼约婚，今何不仍求之？彼兵若至，内外夹攻，操不难破也。布从其计，即日修书，就着二人前去。许汜曰：“须得一军引路冲出方好。”布令张辽、郝萌两个引兵一千，送出隘口。是夜二更，张辽在前，郝萌在后，保着许汜、王楷杀出城去。抹过玄德寨，众将追赶不及，已出隘口。郝萌将五百人，跟许汜、王楷而去。张辽引一半军回来，到隘口时，云长拦住。未及交锋，高顺引兵出城救应，接入城中去了。且说许汜、王楷至寿春，拜见袁术，呈上书信。术曰：“前者杀吾使命，赖我婚姻！今又来相问，何也？”汜曰：“此为曹操奸计所误，愿明上详之。”术曰：“汝主不因曹兵困急，岂肯以女许我？”楷曰：“明上今不相救，恐唇亡齿寒，亦非明上之福也。”术曰：“奉先反复无信，可先送女，然后发兵。”许汜、王楷只得拜辞，和郝萌回来。到玄德寨边，汜曰：“日间不可过。夜半吾二人先行，郝将军断后。”商量停当。夜过玄德寨，许汜、王楷先过去了。郝萌正行之次，张飞出寨拦路。郝萌交马只一合，被张\n\n问题:\n你好\n'}]
    history_list = history_list2
    # a = api_llm(history_list=history_list)
    # print(a)
    for i in api_llm_stream(history_list=history_list):
        print(i, end="")



