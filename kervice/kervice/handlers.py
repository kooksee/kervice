# -*- coding: utf-8 -*-
import asyncio
import time
import ujson as json

from scores.score import score
from utils.app import Application
from utils.http_util import request_get

score = score()


class UrlHandler(object):
    def __init__(self):
        import logging
        self.log = logging.getLogger("UrlHandler")

        # from wacai.utils.app import Application
        # app = Application.current()
        # self._score = app.package("wc#score.score")

    # 灰度分
    def grayInfo_url(self, phone):
        """
        黑中介分数,phone_gray_score
        直接联系人数量,contacts_class1_cnt

        :param phone:
        :return:
        """

        return "http://172.16.5.160:9090/rs/grayInfo/queryGrayPhone/plus_gray_phone/{}".format(phone)

    # 蜜罐
    def usergrid_url(self, phone=None, name=None, idcard=None):
        """
        身份证归属省份
        黑中介分数
        直接联系人数量
        其它
        使用过此身份证的其他手机号统计
        15天内机构查询历史统计
        90天内查询统计

        :param phone:
        :param fields:
        :return:
        """
        # 172.16.10.49/usergrid/search/getfields?name=张振宇&idcard=411082199512080618&phone=18339075202&auth_org=new_score
        # http://172.16.30.15:8040/usergrid/search/getfields?name=张振宇&idcard=532325199504100719&phone=18487177861&auth_org=new_score
        return 'http://172.16.30.15:8040/usergrid/search/getfields?name={name}&idcard={idcard}&phone={phone}&auth_org=new_score'.format(
            phone=phone,
            name=name,
            idcard=idcard
        )

    # 消费标签
    def consummer_tag_url(self, phone):
        """
        LAST_TRA_CT_NM
        TRA_CNT_1ST_CT_NM_PRE12
        FAIL_PAY_PRE6
        TRA_PAY_FAIL_CNT_PRE3
        TRA_CNT_1ST_CT_TRA_AMT_PRE1

        :param phone:
        :return:
        """
        return 'http://172.16.10.115:8090/api/tag/{phone}'.format(
            phone=phone
        )

    # 风控变量
    def riskvar_url(self, phone, fields):
        """
        CPA_RT_DAYS
        CPC_MTHLY_CALL_02_CNT
        CPC_NO_CALL_DAY_CNT
        CPC_H00_05_CNT

        :param phone:
        :param fields:
        :return:
        """
        return 'http://172.16.10.108:8020/api/riskvar/?phone={phone}&fields={fields}'.format(
            phone=phone,
            fields=",".join(fields)
        )

    async def usergrid_data(self, phone=None, name=None, idcard=None):
        """
        获取蜜罐数据
        d_15,d_90,idcard_with_other_phones_cnt,searched_other_org_cnt
        :param phone:
        :return:
        """

        _st = time.time()
        usergrid_url = self.usergrid_url(phone=phone, name=name, idcard=idcard)
        print("蜜罐：", usergrid_url, "\n")
        if not phone:
            return {
                "errMsg": "参数为空",
                "url": usergrid_url,
                "time_used": time.time() - _st
            }

        st, _res = await request_get(usergrid_url)
        if not st:
            return {
                "errMsg": _res,
                "url": usergrid_url,
                "time_used": time.time() - _st
            }

        _d = json.loads(_res)
        return {
            "errMsg": 'ok',
            "url": usergrid_url,
            "time_used": time.time() - _st,
            "data": dict(
                user_province=_d.get("user_province"),
                d15_query_stats=_d.get("d15_query_stats"),
                d90_query_cnt=_d.get("d90_query_cnt"),
                searched_other_org_cnt=_d.get("searched_other_org_cnt"),
                idcard_with_other_phones_cnt=_d.get("idcard_with_other_phones_cnt"),
            )
        }

    async def consummer_tag_data(self, phone):
        "获取消费标签数据"
        """
        ['LAST_TRA_CT_NM', 'TRA_CNT_1ST_CT_NM_PRE12', 'FAIL_PAY_PRE6', 'TRA_PAY_FAIL_CNT_PRE3',
                        'TRA_CNT_1ST_CT_TRA_AMT_PRE1']
        """

        _st = time.time()
        consummer_tag_url = self.consummer_tag_url(phone)
        print(consummer_tag_url)
        print("消费标签：", consummer_tag_url, "\n")
        if not phone:
            return {
                "errMsg": "参数为空",
                "url": consummer_tag_url,
                "time_used": time.time() - _st
            }

        st, _res = await request_get(consummer_tag_url)
        if not st:
            return {
                "errMsg": _res,
                "url": consummer_tag_url,
                "time_used": time.time() - _st
            }

        _d = json.loads(_res)
        if _d['error_code'] != 2000:
            return {
                "errMsg": _d["error_code"],
                "url": consummer_tag_url,
                "data": {},
                "time_used": time.time() - _st
            }

        _d = _d.get("res_data", {}) or {}
        return {
            "errMsg": 'ok',
            "url": consummer_tag_url,
            "time_used": time.time() - _st,
            "data": {i.lower(): j for i, j in _d.items()}
        }

    async def riskvar_data(self, phone):
        "获取风控变量数据"
        """
        ['CPA_RT_DAYS', 'CPC_MTHLY_CALL_02_CNT', 'CPC_NO_CALL_DAY_CNT', 'CPC_H00_05_CNT', 'CPC_H00_CNT',
                         'CPC_H02_CNT', 'CPC_H03_CNT', 'CPC_H04_CNT', 'CPC_H01_CNT']
        """

        _st = time.time()
        riskvar_url = self.riskvar_url(phone,
                                       ['CPA_RT_DAYS', 'CPC_MTHLY_CALL_02_CNT', 'CPC_NO_CALL_DAY_CNT', 'CPC_H05_CNT',
                                        'CPC_H00_CNT',
                                        'CPC_H02_CNT', 'CPC_H03_CNT', 'CPC_H04_CNT', 'CPC_H01_CNT'])
        print("风控变量：", riskvar_url, "\n")
        if not phone:
            return {
                "errMsg": "参数为空",
                "url": riskvar_url,
                "time_used": time.time() - _st
            }

        st, _res = await request_get(riskvar_url)
        if not st:
            return {
                "errMsg": _res,
                "url": riskvar_url,
                "time_used": time.time() - _st
            }

        _d = json.loads(_res)
        if _d["status"] == "fail":
            return {
                "errMsg": _d['msg'],
                "url": riskvar_url,
                "time_used": time.time() - _st,
                "data": {}
            }

        _d = _d["result"]
        _d["CPC_H00_05_CNT"] = _d["CPC_H00_CNT"] + _d["CPC_H01_CNT"] + _d["CPC_H02_CNT"] + _d["CPC_H03_CNT"] + _d[
            "CPC_H04_CNT"] + _d["CPC_H05_CNT"]
        return {
            "errMsg": 'ok',
            "url": riskvar_url,
            "time_used": time.time() - _st,
            "data": {i.lower(): j for i, j in _d.items()}
        }

    async def grayInfo_data(self, phone):
        """
        contacts_class1_cnt: score
        phone_gray_score: order_1_all
        获取灰度分数据
        :param phone:
        :return:
        """

        _st = time.time()
        grayInfo_url = self.grayInfo_url(phone)
        print("灰度分：", grayInfo_url, "\n")
        if not phone:
            return {
                "errMsg": "参数为空",
                "url": grayInfo_url,
                "time_used": time.time() - _st,
            }
        st, _res = await request_get(grayInfo_url)
        if not st:
            return {
                "errMsg": _res,
                "url": grayInfo_url,
                "time_used": time.time() - _st,
            }

        _d = json.loads(_res)
        if _d["code"] != 200:
            return {
                "errMsg": _d['note'],
                "url": grayInfo_url,
                "time_used": time.time() - _st,
                "data": {}
            }

        _d = (json.loads(_d["gray"]) or {}).get("value")
        if not _d:
            return {
                "errMsg": "数据为空",
                "url": grayInfo_url,
                "time_used": time.time() - _st,
                "data": {}
            }

        _d = json.loads(_d) or {}

        return {
            "errMsg": "ok",
            "url": grayInfo_url,
            "time_used": time.time() - _st,
            "data": {
                "contacts_class1_cnt": _d.get("score"),
                "phone_gray_score": _d.get("order_1_all")
            }
        }

    async def wacai_score(self):
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
        :return:
        '''

        _st = time.time()
        _d = {}

        app = Application.current()
        r = app.redis
        st, d = await r.execute('rpop', 'services.post')
        if not st:
            print("st:", d)
            await asyncio.sleep(1)
            return

        if not d:
            print('队列为空 {}'.format(time.time()))
            await asyncio.sleep(1)
            return

        d = json.loads(d)

        _id = d.get("id")
        name = d.get("name")
        phone = d.get("phone")
        idcard = d.get("idcard")

        miguan = await self.usergrid_data(phone=phone, idcard=idcard, name=name)
        miguan_data = miguan.get("data", {})
        x6 = miguan_data.get("d15_query_stats")
        x7 = miguan_data.get("d90_query_cnt")
        x1 = miguan_data.get("user_province")
        x4 = miguan_data.get("searched_other_org_cnt")
        x5 = miguan_data.get("idcard_with_other_phones_cnt")
        _d["蜜罐"] = miguan

        consummer_tag = await self.consummer_tag_data(phone)
        consummer_tag_data = consummer_tag.get("data", {})
        x12 = consummer_tag_data.get("last_tra_ct_nm")
        x16 = consummer_tag_data.get("tra_cnt_1st_ct_tra_amt_pre1")
        x14 = consummer_tag_data.get("fail_pay_pre6")
        x15 = consummer_tag_data.get("tra_pay_fail_cnt_pre3")
        x13 = consummer_tag_data.get("tra_cnt_1st_ct_nm_pre12")
        _d["消费标签"] = consummer_tag

        riskvar = await self.riskvar_data(phone)
        riskvar_data = riskvar.get("data", {})
        x8 = riskvar_data.get("cpa_rt_days")
        x9 = riskvar_data.get("cpc_mthly_call_02_cnt")
        x10 = riskvar_data.get("cpc_no_call_day_cnt")
        x11 = riskvar_data.get("cpc_h00_05_cnt")
        _d["风控变量"] = riskvar

        gray_score = await self.grayInfo_data(phone)
        gray_score_data = gray_score.get("data", {})
        x2 = gray_score_data.get("phone_gray_score")
        x3 = gray_score_data.get("contacts_class1_cnt")
        _d["灰度分"] = gray_score

        _score_time = time.time()
        _score_error = ""
        try:
            _s = score.total_score_batch(
                x1=x1,
                x2=x2,
                x3=x3,
                x4=x4,
                x5=x5,
                x6=x6,
                x7=x7,
                x8=x8,
                x9=x9,
                x10=x10,
                x11=x11,
                x12=x12,
                x13=x13,
                x14=x14,
                x15=x15,
                x16=x16
            ) or 0
        except Exception as e:
            print(e)
            _score_error = str(e)
            _s = 0

        # 保存结果
        asyncio.run_coroutine_threadsafe(
            r.execute(
                'hset',
                'services.get',
                _id,
                str(_s)
            ), asyncio.get_event_loop()
        )

        # 性能指标保存
        _d["create_time"] = d.get("create_time")
        _d["finish_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        asyncio.run_coroutine_threadsafe(
            r.execute(
                'hset',
                'services.properties',
                _id,
                json.dumps({
                    "total_time_used": time.time() - _st,
                    "services": _d,
                    "score_used": time.time() - _score_time,
                    "score_error": _score_error,
                })
            ),
            asyncio.get_event_loop()
        )

        # 参数保存
        __dd = riskvar_data
        __dd.update(miguan_data)
        __dd.update(consummer_tag_data)
        __dd.update(gray_score_data)
        asyncio.run_coroutine_threadsafe(
            r.execute(
                'hset',
                'services.params',
                _id,
                json.dumps({
                    "name": name,
                    "phone": phone,
                    "idcard": idcard,
                    "score_params": __dd
                })
            ),
            asyncio.get_event_loop()
        )


if __name__ == '__main__':
    from utils.log import KLog

    KLog().init_log()
    uh = UrlHandler()
    uh.wacai_score()
    pass
