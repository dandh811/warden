翻译自hackerone

### 基本信息
- 厂商：Shopify
- 资产：accounts.shopify.com
- 漏洞分类：-
- 赏金：$23,500
- 参考链接：https://hackerone.com/reports/867513
### 摘要
攻击者可能绕过shopify的邮件校验，实现对部分用户的账号劫持。
测试人员通过链接： <https://pos-channel.shopifycloud.com/graphql-proxy/admin>，可以提升权限到内部员工账号权限，而不需要邮件确认。

### 发现过程
- 有一个被攻击账号，有商店但是没有shopify id；
- 打开链接：<https://parners.shopify.com>， 创建一个开发商店；
- 在商店创建表单中，你需要更新你的商店电子邮件为一个Shopify中不存在的，但是是你自己的。由于该字段是只读的，需要借助burp抓包工具；
- 将POS添加到您的商店销售渠道；
- 打通 POS > Staff；
- 保存自己的工作页面并使用浏览器复制CURL请求；
- 将CURL有效负载电子邮件字段替换为受害者电子邮件并发送请求；
- 刷新你商店的个人资料页面，你会被提示合并你的帐户，并注意到你没有被要求验证新邮件(受害者的邮件)；
- 继续创建Shopify ID；
- 你现在拥有了Shopify的ID，你可以把它的电子邮件改成你的，因为受害者还可以通过忘记密码恢复；

![](https://hackerone-us-west-2-production-attachments.s3.us-west-2.amazonaws.com/R3SuGsznEDpQys6MkJQanSTt?response-content-disposition=attachment%3B%20filename%3D%22Screen_Shot_2020-05-06_at_7.19.49_PM.png%22%3B%20filename%2A%3DUTF-8%27%27Screen_Shot_2020-05-06_at_7.19.49_PM.png&response-content-type=image%2Fpng&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQGK6FURQRR7SNOUA%2F20201225%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20201225T233131Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEE4aCXVzLXdlc3QtMiJGMEQCIAOPbVFZTCSYJRHBRnSfmulEvMPGbOFqfQEjKIm%2Frh0KAiAaqOBbu8R6pv96XmDYwduddmcMV1nSjGEZU1DaS5IiiSq9Awj3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDAxMzYxOTI3NDg0OSIMAgjNageu%2B4AYsn%2BhKpEDKTNGz5IrBROKCal6CeqoV6dB39MWS%2Ba9OtCCyF6LG8pZGlu%2FMbh%2FXqCxHL05mbwyfI0jDy4ACi2awjHAGZHCkrx82WsgoCQBtaXag1UIA%2FhLeDyHciqrQwNIcztjE2TDv0842uSq8bP9WhVwh%2FjlvdysKSr%2BqyHdzX3UmMKKCn8I%2Bf7bJxhpoGWcsY9l17aqDTM%2BVKW9BoQK6XH29l5iire2q3oClKedgCiJUn5902%2BZpQpZl%2FdUOC0bjYT6ImuE3C4WgrjWfEJDoPkyZg9ZPv633ysF5JnzFhHaVPPgjcTvOPwUR%2FuFUtV2EjqZXVNxlgggz6lKG0iIM69ziaenfcH8xdn3ToYFz0s7FzLHEZa9tu%2BqItgbuTc0lYKTqaZT9%2BVBJsaczKKqqWPm6kXPrf3WuT%2FG1Ebxid1a3gPG85FKtmKkz12%2Ft9h4iJpwDK6eRW18RZXiFA%2F6JWGjS7MhwPr63zAYReFtKtmpHjsK3jThF169caS7SSRQjHkQcsjsFa8Uh7wYf%2Bw2BQu6%2FohoLpEwgcSZ%2FwU67AHbpWjWnWn8l156vPIry5Z3c8qSm1EVXCdJSIVcSnviWrMbZVgLawRgvVpueyglnQQ3zYwU893yNCbEXtE1uLjJZt3DXk%2Fmkd8C1dEH5woK6sbXCRQbZ%2FPignkxZBZDF5TrO42mRWrXWUjnh7Gprs9sF2qXYRAoWrBKlc4sqlfl7f6ak9y4bBYI%2FIuxS66FeMJyF75PUJtw8%2FAKyJsGfQf8qND1GPBveYARb%2FKz7%2F6IaJEkMvEDZayXV9i1OQ7Fk26fXfcwVwA%2BcoUCWvgxPvkJBq1fuxm1HzeQn7jMlgRbilEEChrndaGKLnzb9g%3D%3D&X-Amz-Signature=fd18c2a7a0f19ad3880cd70a555aa60aa328ffff477f283afbb59b88d08e5c86)
### 整改建议

### 漏洞危害
账号劫持

