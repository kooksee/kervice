#!/usr/bin/env python
# encoding: utf-8






import json

import numpy as np
import pandas as pd


class score():
    def __init__(self):
        # coef = [-1.04128015, -0.86403617, -0.33177738, -0.30861044, -0.82229621, -0.54383166, -0.36762961,
        #         -0.38785034, -0.30133738, -0.34098275, -0.68974096, 3.15786664, -0.41576338, -1.31507229,
        #         -0.71994256, -1.34418225]
        # coef_weight
        self.coef = [-1.05915441, -0.87254796, -0.34983982, -0.26579408, -0.70128672, -0.5466186, -0.36810323,
                     -0.4011496,
                     -0.19946099, -0.41391615, -0.67263089, 2.58784098, 0, -1.13035362, -0.78249297, -1.34318885]
        # intercept = [0.01670796]
        # intercept_weight
        self.intercept = [-2.78702812]
        self.se_woe_list = [['user_province', 'multiclass', '西藏自治区、河北省、吉林省、广西壮族自治区、重庆市、9999999.0', -0.320387144],
                            ['user_province', 'multiclass', '海南省、山西省、四川省、甘肃省、贵州省、湖南省、江西省、辽宁省、云南省、湖北省、黑龙江省、宁夏回族自治区',
                             -0.1112517869999999], ['user_province', 'multiclass', '山东省、青海省、福建省', 0.02111949],
                            ['user_province', 'multiclass', '安徽省、河南省、陕西省、内蒙古自治区、广东省', 0.15174221400000001],
                            ['user_province', 'multiclass', '天津市、浙江省、江苏省', 0.386051606],
                            ['user_province', 'multiclass', '新疆维吾尔自治区、北京市', 0.557171596],
                            ['user_province', 'multiclass', '上海市', 0.901807143],
                            ['phone_gray_score', 'continuous', '(-0.001, 7.0]', -0.8631598090000001],
                            ['phone_gray_score', 'continuous',
                             '(7.0, 10.0]、(10.0, 12.0]、(12.0, 15.0]、(15.0, 20.0]、(20.0, 25.0]、(25.0, 29.0]、(29.0, 34.0]、(34.0, 38.0]、(38.0, 42.0]、(42.0, 47.0]、(47.0, 51.0]、(51.0, 55.0]、(55.0, 58.0]、(58.0, 61.0]、(61.0, 64.0]',
                             -0.000763233],
                            ['phone_gray_score', 'continuous',
                             '(64.0, 66.0]、(66.0, 71.0]、(71.0, 75.0]、(75.0, 100.0]、(100.0, 9999999.0]',
                             0.180851955],
                            ['phone_gray_score', 'continuous', '9999999.0', 0.41118422600000004],
                            ['contacts_class1_cnt', 'continuous', '(0.999, 2.0]', 0.383956301],
                            ['contacts_class1_cnt', 'continuous', '(2.0, 4.0]、(4.0, 6.0]、(6.0, 12.0]', 0.184673776],
                            ['contacts_class1_cnt', 'continuous', '(12.0, 30.0]、(30.0, 47.0]、(47.0, 62.0]',
                             -0.047013232],
                            ['contacts_class1_cnt', 'continuous',
                             '(62.0, 76.0]、(76.0, 90.0]、(90.0, 104.0]、(104.0, 121.0]、(121.0, 138.0]、(138.0, 159.0]、(159.0, 183.0]、(183.0, 211.0]、(211.0, 248.0]、(248.0, 296.0]、(296.0, 365.0]',
                             -0.133708661],
                            ['contacts_class1_cnt', 'continuous', '(365.0, 500.0]、(500.0, 3936.0]、(3936.0, 9999999.0]',
                             0.144203681],
                            ['contacts_class1_cnt', 'continuous', '9999999.0', 0.406360714],
                            ['searched_org_other_cnt', 'continuous', '(-0.028, 2.7]、9999999.0', 0.131116945],
                            ['searched_org_other_cnt', 'continuous', '(2.7, 5.4]、(5.4, 8.1]、(8.1, 10.8]、(10.8, 13.5]',
                             -0.441846843], ['searched_org_other_cnt', 'continuous',
                                             '(24.3, 27]、(18.9, 21.6]、(21.6, 24.3]、(13.5, 16.2]、(16.2, 18.9]、(27, 9999999.0]',
                                             -0.533354737],
                            ['idcard_with_other_phones_cnt', 'continuous', '(-0.006, 0.5]、9999999.0', 0.056371715],
                            ['idcard_with_other_phones_cnt', 'continuous', '(0.5, 1.0]', -0.45525617700000004],
                            ['idcard_with_other_phones_cnt', 'continuous',
                             '(2.5, 3.0]、(3.5, 4.0]、(1.5, 2.0]、(4.0, 9999999.0]',
                             -0.901002162], ['d_15_query_stats', 'continuous', '(0.987, 2.2]', 0.015666456000000002],
                            ['d_15_query_stats', 'continuous', '(2.2, 3.4]', -0.398971522],
                            ['d_15_query_stats', 'continuous', '(3.4, 4.6]', -0.607717243],
                            ['d_15_query_stats', 'continuous', '(4.6, 5.8]、(5.8, 7.0]', -0.923907424],
                            ['d_15_query_stats', 'continuous',
                             '(7.0, 8.2]、(10.6, 11.8]、(11.8, 13.0]、(8.2, 9.4]、(9.4, 10.6]、(13.0, 9999999.0]',
                             -1.3867672130000002],
                            ['d_15_query_stats', 'continuous', '9999999.0', 0.203129604],
                            ['d_90_query_cnt', 'continuous', '(-0.001, 1.0]、9999999.0', 0.29872201800000003],
                            ['d_90_query_cnt', 'continuous', '(1.0, 2.0]', 0.06934287],
                            ['d_90_query_cnt', 'continuous', '(2.0, 3.0]、(3.0, 5.0]', -0.134171718],
                            ['d_90_query_cnt', 'continuous', '(5.0, 38.0]、(38.0, 9999999.0]', -0.538571566],
                            ['CPA_RT_DAYS', 'continuous', '(2.999, 296.0]', -0.729392261],
                            ['CPA_RT_DAYS', 'continuous', '(296.0, 432.0]', -0.607136443],
                            ['CPA_RT_DAYS', 'continuous', '(432.0, 561.0]、(561.0, 675.0]', -0.303082401],
                            ['CPA_RT_DAYS', 'continuous', '(675.0, 783.0]、(783.0, 897.4]、(897.4, 1022.0]',
                             -0.20429150399999998],
                            ['CPA_RT_DAYS', 'continuous', '(1022.0, 1125.0]、(1125.0, 1237.0]、(1237.0, 1370.0]',
                             -0.152848352],
                            ['CPA_RT_DAYS', 'continuous',
                             '(1370.0, 1501.0]、(1501.0, 1650.0]、(1650.0, 1811.0]、(1811.0, 1972.0]、(1972.0, 2207.0]',
                             -0.017359114],
                            ['CPA_RT_DAYS', 'continuous', '(2207.0, 2482.0]、(2482.0, 2793.3]', 0.095954136],
                            ['CPA_RT_DAYS', 'continuous',
                             '(2793.3, 3212.0]、(3212.0, 3797.0]、(3797.0, 7506.0]、9999999.0、(7506.0, 9999999.0]',
                             0.187528146],
                            ['CPC_MTHLY_CALL_02_CNT', 'continuous', '(-0.001, 1.0]', -0.39129590399999997],
                            ['CPC_MTHLY_CALL_02_CNT', 'continuous', '(1.0, 3.0]', -0.260388202],
                            ['CPC_MTHLY_CALL_02_CNT', 'continuous', '(3.0, 5.0]', -0.120871245],
                            ['CPC_MTHLY_CALL_02_CNT', 'continuous',
                             '(5.0, 8.0]、(8.0, 96.0]、9999999.0、(96.0, 9999999.0]',
                             0.19554986800000002],
                            ['CPC_NO_CALL_DAY_CNT', 'continuous', '(-2.001, -1.0]、(-1.0, 0.0]', 0.261418711],
                            ['CPC_NO_CALL_DAY_CNT', 'continuous', '(0.0, 1.0]、(1.0, 3.0]、(3.0, 6.0]、(6.0, 11.0]',
                             -0.129791297],
                            ['CPC_NO_CALL_DAY_CNT', 'continuous', '(11.0, 19.0]、(19.0, 30.0]、(30.0, 52.0]',
                             -0.30833365100000004],
                            ['CPC_NO_CALL_DAY_CNT', 'continuous', '(52.0, 626.0]、(626.0, 9999999.0]',
                             -0.5055181129999999],
                            ['CPC_NO_CALL_DAY_CNT', 'continuous', '9999999.0', 0.232894933],
                            ['CPC_H00_05_CNT', 'continuous', '(-0.001, 1.0]', 0.318527528],
                            ['CPC_H00_05_CNT', 'continuous', '(1.0, 3.0]、(3.0, 4.0]、(4.0, 6.0]、(6.0, 8.0]、(8.0, 10.0]',
                             0.114524334],
                            ['CPC_H00_05_CNT', 'continuous',
                             '(10.0, 13.0]、(13.0, 16.0]、(16.0, 19.0]、(19.0, 23.0]、(23.0, 28.0]、(28.0, 33.0]',
                             -0.06252503200000001],
                            ['CPC_H00_05_CNT', 'continuous', '(33.0, 40.0]、(40.0, 49.0]、(49.0, 61.0]、(61.0, 77.0]',
                             -0.253317356],
                            ['CPC_H00_05_CNT', 'continuous', '(77.0, 100.0]', -0.37621549200000004],
                            ['CPC_H00_05_CNT', 'continuous', '(100.0, 140.0]、(140.0, 225.0]', -0.487186275],
                            ['CPC_H00_05_CNT', 'continuous', '(22.05, 1868.0]、(1868.0, 9999999.0]', -0.627187982],
                            ['CPC_H00_05_CNT', 'continuous', '9999999.0', 0.232894933],
                            ['LAST_TRA_CT_NM', 'multiclass', '四线城市、9999999.0', -0.151072176],
                            ['LAST_TRA_CT_NM', 'multiclass', '三线城市、其他、一线城市、新一线城市、五线城市、二线城市', 0.136435483],
                            ['TRA_CNT_1ST_CT_NM_PRE12', 'multiclass', '四线城市、五线城市', -0.39974599],
                            ['TRA_CNT_1ST_CT_NM_PRE12', 'multiclass', '9999999.0', -0.15048502800000002],
                            ['TRA_CNT_1ST_CT_NM_PRE12', 'multiclass', '三线城市、其他', 0.003757155],
                            ['TRA_CNT_1ST_CT_NM_PRE12', 'multiclass', '二线城市、新一线城市、一线城市', 0.20393882100000002],
                            ['FAIL_PAY_PRE6', 'continuous', '(-0.001, 1.0]、(1.0, 3.0]、(3.0, 6.0]、(6.0, 16.0]',
                             0.257422131],
                            ['FAIL_PAY_PRE6', 'continuous', '(16.0, 840.0]、9999999.0、(840.0, 9999999.0]',
                             -0.19269244600000002],
                            ['TRA_PAY_FAIL_CNT_PRE3', 'continuous', '(-0.523, 52.2]', 0.167496543],
                            ['TRA_PAY_FAIL_CNT_PRE3', 'continuous',
                             '(52.2, 104.4]、(365.4, 417.6]、(313.2, 365.4]、(261, 313.2]、(156.6, 208.8]、(208.8, 261]、(104.4, 156.6]',
                             -1.565631975],
                            ['TRA_PAY_FAIL_CNT_PRE3', 'continuous', '(469.8, 522.0]、9999999.0、(522.0, 9999999.0]',
                             -0.14807661800000002],
                            ['TRA_CNT_1ST_CT_TRA_AMT_PRE1', 'continuous', '(-0.001, 153.426]', -0.16345079],
                            ['TRA_CNT_1ST_CT_TRA_AMT_PRE1', 'continuous', '(153.426, 1000.0]、(1000.0, 2850.0]',
                             0.145735287],
                            ['TRA_CNT_1ST_CT_TRA_AMT_PRE1', 'continuous',
                             '(2850.0, 7537.068]、(7537.068, 584806.22]、(584806.22, 9999999.0]', 0.44361410799999995],
                            ['TRA_CNT_1ST_CT_TRA_AMT_PRE1', 'continuous', '9999999.0', -0.161802891]]
        self.bins__ = [
            [-0.001, 7.0, 10.0, 12.0, 15.0, 20.0, 25.0, 29.0, 34.0, 38.0, 42.0, 47.0, 51.0, 55.0, 58.0, 61.0, 64.0,
             66.0, 71.0, 75.0, 100.0, 9999999.0],
            [0.999, 2.0, 4.0, 6.0, 12.0, 30.0, 47.0, 62.0, 76.0, 90.0, 104.0, 121.0, 138.0, 159.0, 183.0, 211.0, 248.0,
             296.0, 365.0, 500.0, 3936.0, 9999999.0],
            [-0.028, 2.7, 5.4, 8.1, 10.8, 13.5, 16.2, 18.9, 21.6, 24.3, 27.0, 9999999.0],
            [-0.006, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 9999999.0],
            [0.987, 2.2, 3.4, 4.6, 5.8, 7.0, 8.2, 9.4, 10.6, 11.8, 13.0, 9999999.0],
            [-0.001, 1.0, 2.0, 3.0, 5.0, 38.0, 9999999.0],
            [2.999, 296.0, 432.0, 561.0, 675.0, 783.0, 897.4, 1022.0, 1125.0, 1237.0, 1370.0, 1501.0, 1650.0, 1811.0,
             1972.0, 2207.0, 2482.0, 2793.3, 3212.0, 3797.0, 7506.0, 9999999.0],
            [-0.001, 1.0, 3.0, 5.0, 8.0, 96.0, 9999999.0],
            [-2.001, -1.0, 0.0, 1.0, 3.0, 6.0, 11.0, 19.0, 30.0, 52.0, 626.0, 9999999.0],
            [-0.001, 1.0, 3.0, 4.0, 6.0, 8.0, 10.0, 13.0, 16.0, 19.0, 22.05, 23.0, 28.0, 33.0, 40.0, 49.0, 61.0, 77.0,
             100.0, 140.0, 225.0, 1868.0, 9999999.0], [-0.001, 1.0, 3.0, 6.0, 16.0, 840.0, 9999999.0],
            [-0.523, 52.2, 104.4, 156.6, 208.8, 261.0, 313.2, 365.4, 417.6, 469.8, 522.0, 9999999.0],
            [-0.001, 153.426, 1000.0, 2850.0, 7537.068, 584806.22, 9999999.0]]
        self.segment_woe_iv_selected = pd.DataFrame(self.se_woe_list, columns=['name', 'type', 'segment', 'woe'])

    def city_to_type(self, x):
        """
        手机号码所对应城市的划分
        :param x: 手机号码所对应城市
        :return: 手机号码所对应城市的划分等级
        """

        if x in [u'上海市', u'北京市', u'广州市', u'深圳市']:
            return u'一线城市'
        elif x in [u'成都市', u'杭州市', u'武汉市', u'天津市', u'南京市', u'重庆市', u'西安市', u'长沙市', u'青岛市', u'沈阳市', u'大连市', u'厦门市',
                   u'苏州市', u'宁波市', u'无锡市']:
            return u'新一线城市'
        elif x in [u'福州市', u'合肥市', u'郑州市', u'哈尔滨', u'佛山市', u'济南市', u'东莞市', u'昆明市', u'太原市', u'南昌市', u'南宁市', u'温州市',
                   u'石家庄市', u'长春市', u'泉州市', u'贵阳市', u'常州市', u'珠海市', u'金华市', u'烟台市', u'海口市', u'惠州市', u'乌鲁木齐市', u'徐州市',
                   u'嘉兴市', u'潍坊市', u'洛阳市', u'南通市', u'扬州市', u'汕头市'
                   ]:
            return u'二线城市'
        elif x in [u'兰州市', u'桂林市', u'三亚市', u'呼和浩特市', u'绍兴市', u'泰州市', u'银川市', u'中山市', u'保定市', u'西宁市', u'芜湖市', u'赣州市',
                   u'绵阳市', u'漳州市', u'莆田市', u'威海市', u'邯郸市', u'临沂市', u'唐山市', u'台州市', u'宜昌市', u'湖州市', u'包头市', u'济宁市',
                   u'盐城市', u'鞍山市', u'廊坊市', u'衡阳市', u'秦皇岛市', u'吉林市', u'大庆市', u'淮安市', u'丽江市', u'揭阳市', u'荆州市', u'连云港市',
                   u'张家口市', u'遵义市', u'上饶市', u'龙岩市', u'衢州市', u'赤峰市', u'湛江市', u'运城市', u'鄂尔多斯市', u'岳阳市', u'安阳市', u'株洲市',
                   u'镇江市', u'淄博市', u'郴州市', u'南平市', u'齐齐哈尔市', u'常德市', u'柳州市', u'咸阳市', u'南充市', u'泸州市', u'蚌埠市', u'邢台市',
                   u'舟山市', u'宝鸡市', u'德阳市', u'抚顺市', u'宜宾市', u'宜春市', u'怀化市', u'榆林市', u'梅州市', u'呼伦贝尔市'
                   ]:
            return u'三线城市'
        elif x in [u'临汾市', u'南阳市', u'新乡市', u'肇庆市', u'丹东市', u'德州市', u'菏泽市', u'九江市', u'江门市 ', u'黄山市', u'渭南市', u'营口市',
                   u'娄底市', u'永州市 ', u'邵阳市', u'清远市', u'大同市', u'枣庄市', u'北海市', u'丽水市', u'孝感市', u'沧州市', u'马鞍山', u'聊城市',
                   u'三明市', u'开封市', u'锦州市', u'汉中市', u'商丘市', u'泰安市', u'通辽市', u'牡丹江', u'曲靖市', u'东营市', u'韶关市', u'拉萨市',
                   u'襄阳市', u'湘潭市', u'盘锦市', u'驻马店市', u'酒泉市', u'安庆市', u'宁德市', u'四平市', u'晋中市', u'滁州市', u'衡水市', u'佳木斯',
                   u'茂名市', u'十堰市', u'宿迁市', u'潮州市', u'承德市', u'葫芦岛市', u'黄冈市', u'本溪市', u'绥化市', u'萍乡市', u'许昌市', u'日照市',
                   u'铁岭市', u'大理州', u'淮南市', u'延边州', u'咸宁市', u'信阳市', u'吕梁市', u'辽阳市', u'朝阳市', u'恩施州', u'达州市 ', u'益阳市 ',
                   u'平顶山', u'六安市', u'延安市', u'梧州市', u'白山市', u'阜阳市', u'铜陵市 ', u'河源市', u'玉溪市 ', u'黄石市', u'通化市', u'百色市',
                   u'乐山市 ', u'抚州市 ', u'钦州市', u'阳江市', u'池州市 ', u'广元市'
                   ]:
            return u'四线城市'
        elif x in [u'滨州市', u'阳泉市', u'周口市', u'遂宁市', u'吉安市', u'长治市', u'铜仁市', u'鹤岗市', u'攀枝花市', u'昭通市', u'云浮市', u'伊犁州',
                   u'焦作市', u'凉山州', u'黔西南州', u'广安市', u'新余市', u'锡林郭勒', u'宣城市', u'兴安盟', u'红河州 ', u'眉山市', u'巴彦淖尔', u'双鸭山市 ',
                   u'景德镇市 ', u'鸡西市', u'三门峡市', u'宿州市', u'汕尾市', u'阜新市', u'张掖市', u'玉林市', u'乌兰察布', u'鹰潭市', u'黑河市', u'伊春市',
                   u'贵港市 ', u'漯河市', u'晋城市', u'克拉玛依', u'随州市', u'保山市', u'濮阳市', u'文山州 ', u'嘉峪关市', u'六盘水市', u'乌海市', u'自贡市',
                   u'松原市', u'内江市', u'黔东南州', u'鹤壁市', u'德宏州', u'安顺市', u'资阳市', u'鄂州市', u'忻州市', u'荆门市', u'淮北市', u'毕节市',
                   u'巴音郭楞', u'防城港', u'天水市', u'黔南州', u'阿坝州', u'石嘴山市', u'安康市', u'亳州市 ', u'昌吉州', u'普洱市', u'楚雄州', u'白城市',
                   u'贺州市', u'哈密市', u'来宾市', u'庆阳市', u'河池市', u'张家界', u'雅安市', u'辽源市', u'湘西州', u'朔州市', u'临沧市', u'白银市',
                   u'塔城地区', u'莱芜市', u'迪庆州', u'喀什地区', u'甘孜州', u'阿克苏', u'武威市', u'巴中市', u'平凉市', u'商洛市', u'七台河', u'金昌市',
                   u'中卫市', u'阿勒泰', u'铜川市', u'海西州', u'吴忠市', u'固原市', u'吐鲁番', u'阿拉善盟', u'博尔塔拉州', u'定西市', u'西双版纳', u'陇南市',
                   u'大兴安岭', u'崇左市', u'日喀则', u'临夏州', u'林芝市', u'海东市', u'怒江州', u'和田地区', u'昌都市', u'儋州市', u'甘南州', u'山南市',
                   u'海南州', u'海北州', u'玉树州', u'阿里地区', u'那曲地区', u'黄南州', u'克孜勒苏州 ', u'果洛州', u'三沙市'
                   ]:
            return u'五线城市'
        elif x is np.nan:
            return None
        elif x is not None:
            return u'其他'
        else:
            return None

    def value_to_woe(self, x, var_multiclass):
        X = x.fillna('9999999.0')
        X = x.replace(9999999.0, '9999999.0')
        for col in var_multiclass['name'].unique():
            d = {}
            a = var_multiclass[var_multiclass['name'] == col][['segment'] + ['woe']]
            b = a.segment.str.split('、')
            for i in range(len(a)):
                for j in range(len(b.iloc[i])):
                    d[b.iloc[i][j]] = a.iloc[i, 1]
            try:
                X[col] = X[col].astype('int').astype('str').map(d)
            except:
                X[col] = X[col].map(d)
        x = X

        return x

    # total_score
    '''
    odds=P_good/P_bad
    woe=np.log(odds)

    score=np.log(odds)*factor+offset

    The factor and the offset are determined on PayPal standards.
    	a score of 600 corresponds to good/bad odds of 20/1
    	a decrease in the score of 50 points corresponds to a doubling of the good/bad odds
    :
    600=np.log(20)*factor+offset
    650=np.log(40)*factor+offset

    factor=50/np.log(2)
    offset=600-factor*np.log(20)

    '''

    def total_score(self,
                    x1=None,
                    x2=None,
                    x3=None,
                    x4=None,
                    x5=None,
                    x6=None,
                    x7=None,
                    x8=None,
                    x9=None,
                    x10=None,
                    x11=None,
                    x12=None,
                    x13=None,
                    x14=None,
                    x15=None,
                    x16=None):
        '''
        计算总得分
        :param x1:身份证归属省份
        :param x2:黑中介分数
        :param x3:直接联系人数量
        :param x4:产品类型为其他的数量
        :param x5:使用过此身份证的其他手机号统计
        :param x6:15天内机构查询历史统计
        :param x7:90天内查询统计
        :param x8:注册天数
        :param x9:每月呼叫两次以上的号码的数量
        :param x10:无呼叫天数
        :param x11:00到05点通话次数
        :param x12:近1年内最近一笔交易城市（城市中文名）
        :param x13:近12个月第一常用城市（城市中文名）
        :param x14:前6月交易失败次数
        :param x15:前3月余额不足交易失败次数
        :param x16:近1个月第一常用城市总交易金额
        :return: 总得分
        '''
        factor = 50 / np.log(2)
        offset = 600 - factor * np.log(20) * 1.0
        # coef = [-1.04128015, -0.86403617, -0.33177738, -0.30861044, -0.82229621, -0.54383166, -0.36762961,
        #         -0.38785034, -0.30133738, -0.34098275, -0.68974096, 3.15786664, -0.41576338, -1.31507229,
        #         -0.71994256, -1.34418225]
        # coef_weight
        coef = self.coef
        # intercept = [0.01670796]
        # intercept_weight
        intercept = self.intercept
        x = pd.DataFrame([(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, self.city_to_type(x12), self.city_to_type(x13),
                           x14, x15, x16)], columns=self.segment_woe_iv_selected['name'].unique())
        var_continuous = self.segment_woe_iv_selected[self.segment_woe_iv_selected['type'] == 'continuous'][
            ['name'] + ['segment'] + ['woe']]
        var_multiclass = self.segment_woe_iv_selected[self.segment_woe_iv_selected['type'] == 'multiclass'][
            ['name'] + ['segment'] + ['woe']]
        x = x.replace([None], np.nan)
        x = x.replace(-999, np.nan)
        x = x.replace('-999', np.nan)
        # 连续变量
        for col in var_continuous['name'].drop_duplicates():
            group_len = len(var_continuous[var_continuous['name'] == col]['segment'])
            for i in range(0, group_len):
                bins = var_continuous[var_continuous['name'] == col]['segment'].iloc[i]
                bins = bins.replace(']', '').replace('[', '').replace('(', '').replace(')', '').replace('、',
                                                                                                        ',').split(
                    ',')
                # ‘9999999.0’改为缺省值
                bins = [np.nan if _x == '9999999.0' else _x for _x in bins]
                # 字符转为数值
                bins = list(map(float, bins))
                # 去重加排序
                bins = sorted(list(set(bins)))
                if np.isnan(x[col].iloc[0]):
                    if np.isnan(np.max(bins)):
                        x[col].iloc[0] = var_continuous[var_continuous['name'] == col]['woe'].iloc[i]
                        break

                else:
                    if i == 0 and np.nanmin(bins) <= x[col].iloc[0] <= np.nanmax(bins):
                        x[col].iloc[0] = var_continuous[var_continuous['name'] == col]['woe'].iloc[0]
                        break
                    if np.isnan(np.nanmax(bins)) and i == group_len:
                        if 0 < i < group_len - 1 and np.nanmin(bins) < x[col].iloc[0] <= np.nanmax(bins):
                            x[col].iloc[0] = var_continuous[var_continuous['name'] == col]['woe'].iloc[i]
                            break
                        if i == group_len - 1 and np.nanmin(bins) < x[col].iloc[0]:
                            x[col].iloc[0] = var_continuous[var_continuous['name'] == col]['woe'].iloc[i]
                            break
                    else:
                        if 0 < i < group_len and np.nanmin(bins) < x[col].iloc[0] <= np.nanmax(bins):
                            x[col].iloc[0] = var_continuous[var_continuous['name'] == col]['woe'].iloc[i]
                            break
                        if i == group_len and np.nanmin(bins) < x[col].iloc[0]:
                            x[col].iloc[0] = var_continuous[var_continuous['name'] == col]['woe'].iloc[i]
                            break
            if np.isnan(x[col].iloc[0]):
                x[col].iloc[0] = np.min(var_continuous[var_continuous['name'] == col]['woe'])
        # 离散变量

        for col in var_multiclass['name'].unique():
            x = x.fillna('9999999.0')
            x = x.replace(9999999.0, '9999999.0')
            d = {}
            a = var_multiclass[var_multiclass['name'] == col][['segment'] + ['woe']]
            b = a.segment.str.split('、')
            for i in range(len(a)):
                for j in range(len(b.iloc[i])):
                    d[b.iloc[i][j]] = a.iloc[i, 1]
            d = json.loads(json.dumps(d, encoding='utf-8', ensure_ascii=False))
            try:
                x[col] = x[col].astype('int').astype('str').map(d)
            except:
                x[col] = x[col].map(d)
        total_score = factor * (-np.mat(x.iloc[0]) * (np.mat(coef).T) - intercept[0]) + offset
        total_score_value = np.array(total_score)[0][0]
        return total_score_value

    def total_score_batch(self,
                          x1=None,
                          x2=None,
                          x3=None,
                          x4=None,
                          x5=None,
                          x6=None,
                          x7=None,
                          x8=None,
                          x9=None,
                          x10=None,
                          x11=None,
                          x12=None,
                          x13=None,
                          x14=None,
                          x15=None,
                          x16=None):
        '''
        计算总得分
        :param x1:身份证归属省份
        :param x2:黑中介分数
        :param x3:直接联系人数量
        :param x4:产品类型为其他的数量
        :param x5:使用过此身份证的其他手机号统计
        :param x6:15天内机构查询历史统计
        :param x7:90天内查询统计
        :param x8:注册天数
        :param x9:每月呼叫两次以上的号码的数量
        :param x10:无呼叫天数
        :param x11:00到05点通话次数
        :param x12:近1年内最近一笔交易城市（城市中文名）
        :param x13:近12个月第一常用城市（城市中文名）
        :param x14:前6月交易失败次数
        :param x15:前3月余额不足交易失败次数
        :param x16:近1个月第一常用城市总交易金额
        :return: 总得分

        注意点：必须有9999999的组，第一组必须是最小值减去0.001的左开又闭区间，加一组最大数到9999999的左开右闭区间
        批量计算得分
        :param df: 所有所需字段的原始数据，二维表的格式
        :return: 各总得分
        """

        odds=P_good/P_bad
        woe=np.log(odds)

        score=np.log(odds)*factor+offset

        The factor and the offset are determined on PayPal standards.
        	a score of 600 corresponds to good/bad odds of 20/1
        	a decrease in the score of 50 points corresponds to a doubling of the good/bad odds
        :
        600=np.log(20)*factor+offset
        650=np.log(40)*factor+offset

        factor=50/np.log(2)
        offset=600-factor*np.log(20)

        '''
        factor = 50 / np.log(2)
        offset = 600 - factor * np.log(20)

        coef = self.coef
        intercept = self.intercept
        df = pd.DataFrame(
            [(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, self.city_to_type(x12), self.city_to_type(x13),
              x14, x15, x16)], columns=self.segment_woe_iv_selected['name'].unique())
        # 城市按等级划分
        df.LAST_TRA_CT_NM = df.LAST_TRA_CT_NM.apply(lambda x: self.city_to_type(x))
        df.TRA_CNT_1ST_CT_NM_PRE12 = df.TRA_CNT_1ST_CT_NM_PRE12.apply(lambda x: self.city_to_type(x))

        df = df.replace([None], np.nan)
        df = df.replace(-999, np.nan)
        df = df.replace('-999', np.nan)
        var_continuous = self.segment_woe_iv_selected[self.segment_woe_iv_selected['type'] == 'continuous'][
            ['name'] + ['segment'] + ['woe']]
        # 连续变量
        """
        # 确定各个变量bins
        bins__ = []
        for col in var_continuous['name'].drop_duplicates():
            bins_ = []
            group_len = len(var_continuous[var_continuous['name'] == col]['segment'])
            for i in range(0, group_len):
                bins = var_continuous[var_continuous['name'] == col]['segment'].iloc[i]
                bins = bins.replace(']', '').replace('[', '').replace('(', '').replace(')', '').replace('、',
                                                                                                        ',').split(
                    ',')
                bins_.extend(bins)
            bins_ = list(map(float, bins_))
            # 去重加排序
            bins_ = sorted(list(set(bins_)))
            bins__.append(bins_)
        print(bins__)
        """
        for i, col in enumerate(var_continuous['name'].drop_duplicates()):
            df[col] = pd.cut(df[col], bins=self.bins__[i])
        df = df.replace(np.nan, '9999999.0')
        for col in self.segment_woe_iv_selected['name'].unique():
            d = {}
            a = self.segment_woe_iv_selected[self.segment_woe_iv_selected['name'] == col][['segment'] + ['woe']]
            b = a.segment.str.split('、')
            for i in range(len(a)):
                for j in range(len(b.iloc[i])):
                    d[b.iloc[i][j]] = a.iloc[i, 1]
            # d = json.loads(json.dumps(d, encoding='utf-8', ensure_ascii=False))
            try:
                df[col] = df[col].astype('float').astype('str').map(d)
            except:
                df[col] = df[col].astype('str').map(d)
        # df_woe = df.drop(['id'],axis=1)
        df_woe = df
        # 矩阵运算
        score = (np.mat(df_woe) * (np.mat(coef).T) + intercept[0] * np.ones(
            (df_woe.shape[0], 1))) * (-factor) + offset * np.ones((df_woe.shape[0], 1))
        score = np.array(score)[0][0]
        # #循环
        # score=[]
        # for i in range(len(df_woe)):
        #     score_mid=-factor * (np.mat(np.array(df_woe.iloc[i,:])) * (np.mat(coef).T) + intercept[0]) + offset
        #     score.append(score_mid)

        return score


if __name__ == '__main__':
    pass
    # import os
    # from datetime import datetime
    #
    # local_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    # a = datetime.now()
    # segment_woe_iv_selected = pd.read_csv('C:/Users/Administrator/PycharmProjects/wacai_program/model_file/group_bins_adjust20170515.csv', encoding='gbk')
    # df = pd.read_csv('C:/Users/Administrator/PycharmProjects/wacai_program/data/data_all_selected_20170510.csv',
    #                  encoding='gbk')

    # #一个一个循环计算
    # score_all = []
    # for i in range(len(df)):
    # # i=15688
    # #     print(i)
    #     score_example = score().total_score(
    #         x1=df.ix[i, 1],
    #         x2=df.ix[i, 2],
    #         x3=df.ix[i, 3],
    #         x4=df.ix[i, 4],
    #         x5=df.ix[i, 5],
    #         x6=df.ix[i, 6],
    #         x7=df.ix[i, 7],
    #         x8=df.ix[i, 8],
    #         x9=df.ix[i, 9],
    #         x10=df.ix[i, 10],
    #         x11=df.ix[i, 11],
    #         x12=df.ix[i, 12],
    #         x13=df.ix[i, 13],
    #         x14=df.ix[i, 14],
    #         x15=df.ix[i, 15],
    #         x16=df.ix[i, 16])
    #     # print(score_example)
    #     score_all.append(score_example)
    # df['score']= score_all
    # df.to_csv('C:/Users/Administrator/PycharmProjects/wacai_program/data/score_new_weight.csv',index=False)

    # 分批量计算
    import time

    st = time.time()
    # score_1 = score().total_score(**{'x1': u'安徽省', 'x2': 12, 'x3': 168, 'x4': 1, 'x5': 1, 'x6': 1, 'x7': 1, 'x8': 90, 'x9': 21, 'x10': 6, 'x11': 11, 'x12': u'贵州省', 'x13': u'山西省', 'x14': 16, 'x15': 10, 'x16': -999})
    score_dict = {'x1': None, 'x2': 13, 'x3': 168, 'x4': 1, 'x5': 1, 'x6': 1, 'x7': 1, 'x8': 90, 'x9': 21, 'x10': 6,
                  'x11': 11, 'x12': u'贵州省', 'x13': u'山西省', 'x14': 16, 'x15': 10, 'x16': -999}
    score_2 = score().total_score_batch(**score_dict)
    # print score_1
    print(score_2, time.time() - st)
    # df['score'] = score
    # df.to_csv('C:/Users/Administrator/PycharmProjects/wacai_program/data/score_batch_new.csv', index=False)
    #
    #
    #
    # b=datetime.now()
    # print((b-a))
