# /usr/bin/env python
# -*- coding: utf-8 -*-

import execjs
import requests
from googletrans import Translator

Translate_Languages = [
    ('gv', 'Manx', '马恩岛语'),
    ('or', 'Oriya', '奥利亚语'),
    ('ko', 'Korean', '朝鲜语、韩语'),
    ('ja', 'Japanese', '日语'),
    ('bg', 'Bulgarian', '保加利亚语'),
    ('km', 'Central Khmer', '高棉语'),
    ('ch', 'Chamorro', '查莫罗语'),
    ('gn', 'Guarani', '瓜拉尼语'),
    ('ht', 'Haitian; Haitian Creole', '海地克里奥尔语'),
    ('ii', 'Sichuan Yi; Nuosu', '四川彝语（诺苏语'),
    ('ki', 'Kikuyu; Gikuyu', '基库尤语'),
    ('ho', 'Hiri Motu', '希里莫图语'),
    ('eo', 'Esperanto', '世界语'),
    ('jv', 'Javanese', '爪哇语'),
    ('os', 'Ossetian; Ossetic', '奥塞梯语'),
    ('ta', 'Tamil', '泰米尔语'),
    ('lb', 'Luxembourgish; Letzeburgesch', '卢森堡语'),
    ('rm', 'Romansh', '罗曼什语'),
    ('nl', 'Dutch; Flemish', '荷兰语'),
    ('is', 'Icelandic', '冰岛语'),
    ('gu', 'Gujarati', '古吉拉特语'),
    ('lu', 'Luba-Katanga', '卢巴语'),
    ('vi', 'Vietnamese', '越南语'),
    ('ia', 'Interlingua (International Auxiliary Language Association)', '国际语A'),
    ('fr', 'French', '法语'),
    ('pi', 'Pali', '巴利语'),
    ('xh', 'Xhosa', '科萨语'),
    ('av', 'Avaric', '阿瓦尔语'),
    ('ne', 'Nepali', '尼泊尔语'),
    ('ik', 'Inupiaq', '依努庇克语'),
    ('lg', 'Ganda', '卢干达语'),
    ('nv', 'Navajo; Navaho', '纳瓦霍语'),
    ('nd', 'Ndebele, North; North Ndebele', '北恩德贝勒语'),
    ('no', 'Norwegian', '挪威语'),
    ('so', 'Somali', '索马里语'),
    ('tt', 'Tatar', '塔塔尔语'),
    ('ar', 'Arabic', '阿拉伯语'),
    ('ts', 'Tsonga', '宗加语'),
    ('cr', 'Cree', '克里语'),
    ('hz', 'Herero', '赫雷罗语'),
    ('it', 'Italian', '意大利语'),
    ('nb', 'Bokmål, Norwegian; Norwegian Bokmål', '书面挪威语'),
    ('ng', 'Ndonga', '恩敦加语'),
    ('sl', 'Slovenian', '斯洛文尼亚语'),
    ('sq', 'Albanian', '阿尔巴尼亚语'),
    ('aa', 'Afar', '阿法尔语'),
    ('kk', 'Kazakh', '哈萨克语'),
    ('ro', 'Romanian; Moldavian; Moldovan', '罗马尼亚语'),
    ('bm', 'Bambara', '班巴拉语'),
    ('ky', 'Kirghiz; Kyrgyz', '吉尔吉斯语'),
    ('lv', 'Latvian', '拉脱维亚语'),
    ('mn', 'Mongolian', '蒙古语'),
    ('wo', 'Wolof', '沃洛夫语'),
    ('ba', 'Bashkir', '巴什基尔语'),
    ('mk', 'Macedonian', '马其顿语'),
    ('ru', 'Russian', '俄语'),
    ('ka', 'Georgian', '格鲁吉亚语'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian', '新挪威语'),
    ('he', 'Hebrew', '希伯来语'),
    ('bo', 'Tibetan', '藏语'),
    ('cy', 'Welsh', '威尔士语'),
    ('da', 'Danish', '丹麦语'),
    ('sd', 'Sindhi', '信德语'),
    ('ab', 'Abkhazian', '阿布哈兹语'),
    ('gl', 'Galician', '加利西亚语'),
    ('pt', 'Portuguese', '葡萄牙语'),
    ('mi', 'Maori', '毛利语'),
    ('vo', 'Volapük', '沃拉普克语'),
    ('ln', 'Lingala', '林加拉语'),
    ('wa', 'Walloon', '沃伦语'),
    ('id', 'Indonesian', '印尼语'),
    ('ti', 'Tigrinya', '提格里尼亚语'),
    ('tr', 'Turkish', '土耳其语'),
    ('ig', 'Igbo', '伊博语'),
    ('ur', 'Urdu', '乌尔都语'),
    ('fj', 'Fijian', '斐济语'),
    ('io', 'Ido', '伊多语'),
    ('hr', 'Croatian', '克罗地亚语'),
    ('kw', 'Cornish', '康沃尔语'),
    ('to', 'Tonga (Tonga Islands)', '汤加语'),
    ('ie', 'Interlingue; Occidental', '国际语E'),
    ('iu', 'Inuktitut', '因纽特语'),
    ('cs', 'Czech', '捷克语'),
    ('kg', 'Kongo', '刚果语'),
    ('rw', 'Kinyarwanda', '卢旺达语'),
    ('ha', 'Hausa', '豪萨语'),
    ('st', 'Sotho, Southern', '南索托语'),
    ('kv', 'Komi', '科米语'),
    ('sc', 'Sardinian', '萨丁尼亚语'),
    ('na', 'Nauru', '瑙鲁语'),
    ('sk', 'Slovak', '斯洛伐克语'),
    ('bs', 'Bosnian', '波斯尼亚语'),
    ('su', 'Sundanese', '巽他语'),
    ('ug', 'Uighur; Uyghur', '维吾尔语'),
    ('ak', 'Akan', '阿坎语'),
    ('zh', 'Chinese', '中文'),
    ('se', 'Northern Sami', '北萨米语'),
    ('dz', 'Dzongkha', '不丹语'),
    ('fy', 'Western Frisian', '弗里西亚语'),
    ('gd', 'Gaelic; Scottish Gaelic', '苏格兰盖尔语'),
    ('es', 'Spanish; Castilian', '西班牙语'),
    ('uk', 'Ukrainian', '乌克兰语'),
    ('ae', 'Avestan', '阿维斯陀语'),
    ('mg', 'Malagasy', '马达加斯加语'),
    ('oj', 'Ojibwa', '奥吉布瓦语'),
    ('mh', 'Marshallese', '马绍尔语'),
    ('sm', 'Samoan', '萨摩亚语'),
    ('sa', 'Sanskrit', '僧加罗语'),
    ('ss', 'Swati', '斯瓦特语'),
    ('sg', 'Sango', '桑戈语'),
    ('as', 'Assamese', '阿萨姆语'),
    ('sr', 'Serbian', '塞尔维亚语'),
    ('la', 'Latin', '拉丁语'),
    ('ks', 'Kashmiri', '克什米尔语'),
    ('am', 'Amharic', '阿姆哈拉语'),
    ('nr', 'Ndebele, South; South Ndebele', '南恩德贝勒语'),
    ('dv', 'Divehi; Dhivehi; Maldivian', '迪维希语'),
    ('ff', 'Fulah', '富拉语'),
    ('ms', 'Malay', '马来语'),
    ('pa', 'Panjabi; Punjabi', '旁遮普语'),
    ('my', 'Burmese', '缅甸语'),
    ('an', 'Aragonese', '阿拉贡语'),
    ('sv', 'Swedish', '瑞典语'),
    ('ce', 'Chechen', '车臣语'),
    ('li', 'Limburgan; Limburger; Limburgish', '林堡语'),
    ('tw', 'Twi', '特威语'),
    ('ee', 'Ewe', '埃维语'),
    ('hi', 'Hindi', '印地语'),
    ('hu', 'Hungarian', '匈牙利语'),
    ('kn', 'Kannada', '卡纳达语'),
    ('bh', 'Bihari languages', '比哈尔语'),
    ('el', 'Greek, Modern (1453-)', '现代希腊语'),
    ('en', 'English', '英语'),
    ('uz', 'Uzbek', '乌兹别克语'),
    ('eu', 'Basque', '巴斯克语'),
    ('ca', 'Catalan; Valencian', '加泰隆语'),
    ('kl', 'Kalaallisut; Greenlandic', '格陵兰语'),
    ('te', 'Telugu', '泰卢固语'),
    ('tn', 'Tswana', '塞茨瓦纳语'),
    ('be', 'Belarusian', '白俄罗斯语'),
    ('fa', 'Persian', '波斯语'),
    ('ay', 'Aymara', '艾马拉语'),
    ('ve', 'Venda', '文达语'),
    ('pl', 'Polish', '波兰语'),
    ('fi', 'Finnish', '芬兰语'),
    ('kj', 'Kuanyama; Kwanyama', '宽亚玛语'),
    ('ps', 'Pushto; Pashto', '普什图语'),
    ('th', 'Thai', '泰语'),
    ('bn', 'Bengali', '孟加拉语'),
    ('oc', 'Occitan (post 1500)', '奥克语'),
    ('tk', 'Turkmen', '土库曼语'),
    ('bi', 'Bislama', '比斯拉马语'),
    ('hy', 'Armenian', '亚美尼亚语'),
    ('rn', 'Rundi', '基隆迪语'),
    ('fo', 'Faroese', '法罗语'),
    ('lt', 'Lithuanian', '立陶宛语'),
    ('mt', 'Maltese', '马耳他语'),
    ('cv', 'Chuvash', '楚瓦什语'),
    ('mr', 'Marathi', '马拉提语'),
    ('co', 'Corsican', '科西嘉语'),
    ('om', 'Oromo', '奥洛莫语'),
    ('za', 'Zhuang; Chuang', '壮语'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', '古教会斯拉夫语'),
    ('tg', 'Tajik', '塔吉克斯坦语'),
    ('si', 'Sinhala; Sinhalese'),
    ('lo', 'Lao', '老挝语'),
    ('qu', 'Quechua', '凯楚亚语'),
    ('et', 'Estonian', '爱沙尼亚语'),
    ('sn', 'Shona', '绍纳语'),
    ('ku', 'Kurdish', '库尔德语'),
    ('ty', 'Tahitian', '塔希提语'),
    ('kr', 'Kanuri', '卡努里语'),
    ('yi', 'Yiddish', '依地语'),
    ('ml', 'Malayalam', '马拉亚拉姆语'),
    ('zu', 'Zulu', '祖鲁语'),
    ('af', 'Afrikaans', '南非语'),
    ('ga', 'Irish', '爱尔兰语'),
    ('yo', 'Yoruba', '约鲁巴语'),
    ('de', 'German', '德语'),
    ('sw', 'Swahili', '斯瓦希里语'),
    ('tl', 'Tagalog', '他加禄语'),
    ('br', 'Breton', '布列塔尼语'),
    ('az', 'Azerbaijani', '阿塞拜疆语')
]


class GoogleTraslate:
    def __init__(self, sl='auto', tl='en'):
        """
        初始化
        :param sl: 待翻译原语种，默认值为auto
        :param tl: 目的翻译语种
        """
        self.sl = sl
        self.tl = tl

    @staticmethod
    def get_short_name(alias):
        for languages in Translate_Languages:
            if alias in languages:
                return languages[0]
        return None

    @staticmethod
    def get_tk(txt):
        """
        生成tk
        """
        ctx = execjs.compile("""
                function TL(a) {
                var k = "";
                var b = 406644;
                var b1 = 3293161072;
                var jd = ".";
                var $b = "+-a^+6";
                var Zb = "+-3^+b+-f";
                for (var e = [], f = 0, g = 0; g < a.length; g++) {
                    var m = a.charCodeAt(g);
                    128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                    e[f++] = m >> 18 | 240,
                    e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                    e[f++] = m >> 6 & 63 | 128),
                    e[f++] = m & 63 | 128)
                }
                a = b;
                for (f = 0; f < e.length; f++) a += e[f],
                a = RL(a, $b);
                a = RL(a, Zb);
                a ^= b1 || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1E6;
                return a.toString() + jd + (a ^ b)
            };
            function RL(a, b) {
                var t = "a";
                var Yb = "+";
                for (var c = 0; c < b.length - 2; c += 3) {
                    var d = b.charAt(c + 2),
                    d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                    d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                    a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
                }
                return a
            }
            """)
        return ctx.call("TL", txt)

    def translate(self, content, sl=None, tl=None):
        """
        翻译 （sl、tl默认None，则为初始化值）
        :param content: 待翻译文本
        :param sl: 待翻译原语种
        :param tl: 期待翻译语种
        """
        if len(content) > 4891:
            raise ValueError("content length must be less than 4891")
        tk = self.get_tk(content)
        if sl is None:
            sl = self.sl
        if tl is None:
            tl = self.tl
        url = f"http://translate.google.cn/translate_a/single?client=t" \
              f"&sl={sl}&tl={tl}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
              f"&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8" \
              f"&source=btn&ssel=3&tsel=3&kc=0&tk={tk}&q={content}&"
        result = None
        ret = requests.get(url)
        if ret.status_code == 200:
            for _ in ret.json():
                if _ and isinstance(_, list):
                    result = "".join([_[i][0] for i in range(len(_)-1)])
                    break
        return result


class GoogleTrans:
    """
    调用googletrans第三方包实现
    """
    def __init__(self, sl='auto', tl='en', **args):
        """
        初始化
        :param :sl 待翻译原语种，默认值为auto
        :param :tl 目的翻译语种
        :param :**args 可选参数
                service_urls=DEFAULT_CLIENT_SERVICE_URLS,   可以默认，也可以提供多个翻译域，会随机选择一个。
                user_agent=DEFAULT_USER_AGENT,
                raise_exception=DEFAULT_RAISE_EXCEPTION,
                proxies: typing.Dict[str, httpcore.SyncHTTPTransport] = None,
                timeout: Timeout = None,
                http2=True,
                use_fallback=False
        """
        self.translator = Translator(**args)
        self.sl = self.__If_zh(sl)
        self.tl = self.__If_zh(tl)

    @staticmethod
    def __If_zh(_language):
        """zh无法识别，需转换为zh_CN"""
        if _language == 'zh':
            _language = 'zh-CN'
        return _language

    def language(self, content):
        """
        检测语种
        :param content: 待检测内容
        :return ret: Detected
        """
        ret = self.translator.detect(content)
        # print(ret.__dict__)
        return ret

    def translate(self, content, sl=None, tl=None, run_max_count=3):
        """
        翻译 （sl、tl默认None，则为初始化值）
        :param content: 待翻译文本
        :param sl: 待翻译原语种
        :param tl: 期待翻译语种
        """
        if sl is None:
            sl = self.sl
        if tl is None:
            tl = self.tl
        result = None
        count = 0
        while True:
            try:
                result = self.translator.translate(content, dest=self.__If_zh(tl), src=self.__If_zh(sl)).text
                break
            except Exception as e:
                print(e)
                count += 1
                if count > run_max_count:
                    break
        return result


def translate_test():
    gg = GoogleTrans(service_urls=['translate.google.cn', 'translate.google.com'])
    # 默认翻译为英语
    content = "根据围棋的外观，有人称它为方圆，这是因为围棋盘围棋谱围棋谱(24张)是方的。棋子、棋盒是圆形的,这是因为围棋分黑白两色。白子如白鹭。围棋还可称枰即棋盘。我们喜欢下围棋。"
    data = gg.translate(content)
    print("汉译音：%s" % data)
    # 汉译西班牙
    rt = gg.translate("我们一起学猫叫", 'zh-CN', 'es')
    print("中文翻译西班牙语：%s" % rt)
    # 检测语种
    dt = gg.language(content)
    print("检测语种：")
    print(dt.__dict__)
    print("language: %s, confidence: %s" % (dt.lang, dt.confidence))

    # # 汉译英
    # gg = GoogleTraslate("zh", "en")
    # rt = gg.translate("我们一起学猫叫")
    # print(rt)
    # # 中文翻译德语
    # gg = GoogleTraslate()
    # rt = gg.translate("我们一起学猫叫", "zh", "de")
    # print(rt)
    # # 日文翻译中文
    # rt = gg.translate('もしある種の能力に喜びを感じるのであれば、あなたがその中で最強であって欲しい', "ja", "zh")
    # print(rt)
    # # 汉译英 段落
    # content = "根据围棋的外观，有人称它为方圆，这是因为围棋盘围棋谱围棋谱(24张)是方的。棋子、棋盒是圆形的,这是因为围棋分黑白两色。白子如白鹭。围棋还可称枰即棋盘。我们喜欢下围棋。"
    # data = GoogleTraslate().translate(content, "zh", "en")
    # print(data)
    # # 获取简称
    # dt = gg.get_short_name("德语")
    # print(dt)


if __name__ == '__main__':
    """ 
    Install:
        python -m pip install googletrans==4.0.0rc1 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
    """
    translate_test()




