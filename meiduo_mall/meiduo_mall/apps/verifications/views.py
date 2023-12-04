import random

from django import http
from django.shortcuts import render
from django.utils.autoreload import logger
from django.views import View
from django_redis import get_redis_connection

from libs.captcha.captcha import captcha
from libs.yuntongxun.ccp_sms import CCP


# Create your views here.

class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, mobile):
        """
        :param reqeust: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 1. 接收参数
        image_code_client = reqeust.GET.get('image_code')
        uuid = reqeust.GET.get('image_code_id')

        # 2. 校验参数
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code': 400,
                                      'errmsg': '缺少必传参数'})

        # 3. 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')

        # 4. 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': 400,
                                      'errmsg': '图形验证码失效'})

        # 5. 删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 6. 对比图形验证码
        # bytes 转字符串
        image_code_server = image_code_server.decode()
        # 转小写后比较
        if image_code_client.lower() != image_code_server.lower():
            return http.JsonResponse({'code': 400,
                                      'errmsg': '输入图形验证码有误'})

        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': 400,
                                      'errmsg': '发送短信过于频繁'})

        # 7. 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)

        # 8. 保存短信验证码
        # # 短信验证码有效期，单位：秒
        # # SMS_CODE_REDIS_EXPIRES = 300
        # redis_conn.setex('sms_code_%s' % mobile,
        #                  300,
        #                  sms_code)
        #
        # # 重新写入send_flag
        # # 60s内是否重复发送的标记
        # # SEND_SMS_CODE_INTERVAL = 60(s)
        # redis_conn.setex('send_flag_%s' % mobile,
        #                  60,
        #                  1)
        # 创建Redis管道
        pl = redis_conn.pipeline()

        # 将Redis请求添加到队列
        pl.setex('sms_%s' % mobile, 300, sms_code)
        pl.setex('send_flag_%s' % mobile, 60, 1)

        # 执行请求
        pl.execute()

        # 9. 发送短信验证码
        # 短信模板
        # SMS_CODE_REDIS_EXPIRES // 60 = 5min
        # SEND_SMS_TEMPLATE_ID = 1
        CCP().send_template_sms(mobile, [sms_code, 5],
                                1)

        print("code: ", sms_code)

        # 10. 响应结果
        return http.JsonResponse({'code': 200,
                                  'errmsg': '发送短信成功'})


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """
        # 生成图片验证码
        text, image = captcha.generate_captcha()

        # 保存图片验证码
        redis_conn = get_redis_connection('verify_code')

        # 图形验证码有效期，单位：秒
        # IMAGE_CODE_REDIS_EXPIRES = 300
        redis_conn.setex('img_%s' % uuid, 300, text)

        # 响应图片验证码
        return http.HttpResponse(image, content_type='imgae/jpg')
