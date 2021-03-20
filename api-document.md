## 1. 请求发送邮箱验证码

### 接口功能

> 请求服务端发送邮箱验证码

### URL

> /api/v1/email_captcha

### 支持格式

> JSON

### HTTP 请求方式

> POST

### 请求参数

> | 参数 | 必选 | 类型   | 说明           |
> | :--- | :--- | :----- | -------------- |
> | mail | ture | string | 需要验证的邮箱 |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                                                                                       |
> | :------- | :------- | :--------------------------------------------------------------------------------------------------------- |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误                                                          |
> | message  | string   | 信息<br>-ok 成功发送<br>-invalid email address 邮箱格式错误<br>-requests are too frequent 请求过于频繁<br> |

## 2. 请求登录

### 接口功能

> 验证验证码并登录

### URL

> /login

### 支持格式

> JSON

### HTTP 请求方式

> POST

### 请求参数

> | 参数 | 必选 | 类型   | 说明       |
> | :--- | :--- | :----- | ---------- |
> | mail | ture | string | 登录邮箱   |
> | code | ture | string | 邮箱验证码 |

### 返回字段

> | 返回字段  | 字段类型 | 说明                                                                                                       |
> | :-------- | :------- | :--------------------------------------------------------------------------------------------------------- |
> | status    | string   | 返回结果状态<br>-success：正常 <br>-failure：错误                                                          |
> | message   | string   | 信息<br>-ok 成功发送<br>-invalid email address 邮箱格式错误<br>-requests are too frequent 请求过于频繁<br> |
> | user_data | string   | 登录成功返回用户信息                                                                                       |
