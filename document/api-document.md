### 登录/注册

<details>
<summary>1. 请求发送邮箱验证码</summary>

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
> | post_id  | string   | 信息<br>-ok 成功发送<br>-invalid email address 邮箱格式错误<br>-requests are too frequent 请求过于频繁<br> |

</details>

<details>
<summary>2. 请求登录</summary>

### 接口功能

> 验证验证码并登录

### URL

> /api/v1/login

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

</details>

### 树洞主体功能

<details>
<summary>3. 发送树洞</summary>

### 接口功能

> 发送新的树洞

### URL

> /api/v1/new_post

### 支持格式

> JSON

### HTTP 请求方式

> POST

### 请求参数

> | 参数    | 必选 | 类型   | 说明                               |
> | :------ | :--- | :----- | ---------------------------------- |
> | token   | ture | string | 存放在 header 中<br>"token":"xxxx" |
> | title   | ture | string | 标题                               |
> | content | ture | string | 内容                               |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | post_id  | int      | 发送成功时返回 文章 的 id                         |

</details>

<details>
<summary>4. 发送爱选修主贴</summary>

### 接口功能

> 发送爱选修主贴

### URL

> /api/v1/sendEmailCode

### HTTP 请求方式

> POST

### 请求参数

> | 参数    | 必选 | 类型   | 说明                               |
> | :------ | :--- | :----- | ---------------------------------- |
> | token   | ture | string | 存放在 header 中<br>"token":"xxxx" |
> | title   | ture | string | 标题                               |
> | content | ture | string | 内容(json)                         |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | post_id  | int      | 发送成功时返回 文章 的 id                         |

</details>

<details>
<summary>5. 获取帖子</summary>

### 接口功能

> 获取树洞内容

### URL

> /api/v1/get_post/<post_id>

### HTTP 请求方式

> GET

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | title    | string   | 文章的标题                                        |
> | content  | string   | 文章的内容                                        |

</details>

<details>
<summary>6. 评论树洞</summary>

### 接口功能

> 评论树洞

### URL

> /api/v1/comment/post/<post_id>

### HTTP 请求方式

> POST

### 支持格式

> JSON

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |
> | body  | ture | string | 评论内容                           |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | id       | int      | 评论的 id                                         |

</details>

<details>
<summary>7. 回复评论</summary>

### 接口功能

> 评论评论(楼中楼)

### URL

> /api/v1/comment/comment/<comment_id>

### HTTP 请求方式

> POST

### 支持格式

> JSON

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |
> | body  | ture | string | 评论内容                           |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | id       | int      | 评论的 id                                         |

</details>

<details>
<summary>8. 获取树洞评论</summary>

### 接口功能

> 获取树洞的评论

### URL

> /api/v1/comment/post/<post_id>

### HTTP 请求方式

> GET

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |

### 返回示例

```json
{
  "data": {
    "0": {
      "body": "7777",
      "id": 7,
      "replied_id": null,
      "replies": [10, 11],
      "timestamps": "Sat, 20 Mar 2021 21:44:39 GMT"
    },
    "1": {
      "body": "8888",
      "id": 8,
      "replied_id": null,
      "replies": [12, 13],
      "timestamps": "Sat, 20 Mar 2021 21:44:44 GMT"
    },
    "2": {
      "body": "99999",
      "id": 9,
      "replied_id": null,
      "replies": [14, 15],
      "timestamps": "Sat, 20 Mar 2021 21:44:48 GMT"
    }
  },
  "status": "success"
}
```

</details>

<details>
<summary>9. 获取评论的回复</summary>

### 接口功能

> 获取评论的回复

### URL

> /api/v1/comment/comment/<comment_id>

### HTTP 请求方式

> GET

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |

### 返回示例

```json
{
  "data": {
    "0": {
      "body": "sub_7",
      "id": 11,
      "replied_id": 7,
      "replies": [16],
      "timestamps": "Sat, 20 Mar 2021 21:45:21 GMT"
    }
  },
  "status": "success"
}
```

</details>

### 管理功能

<details>
<summary>10. 用户提权</summary>

### 接口功能

> 提权某用户权限到管理员

### 权限要求

> su

### URL

> /api/v1/sudo/<user_id>

### HTTP 请求方式

> POST

### 支持格式

> JSON

### 请求参数

> | 参数   | 必选 | 类型   | 说明                               |
> | :----- | :--- | :----- | ---------------------------------- |
> | token  | ture | string | 存放在 header 中<br>"token":"xxxx" |
> | enc_id | ture | string | 使用 su 私钥签名的用户 id          |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |

</details>

<details>
<summary>11. 封禁帖子</summary>

### 接口功能

> 封禁帖子

### 权限要求

> 管理员

### URL

> /api/v1/banPost/<post_id>

### HTTP 请求方式

> POST

### 支持格式

> JSON

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |

</details>

<details>
<summary>12. 封禁评论</summary>

### 接口功能

> 封禁评论

### 权限要求

> 管理员

### URL

> /api/v1/banComment/<comment_id>

### HTTP 请求方式

> POST

### 支持格式

> JSON

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |

</details>

<details>
<summary>13. 获取帖子作者</summary>

### 接口功能

> 获取帖子作者

### 权限要求

> su

### URL

> /api/v1/getAuthor/post/<post_id>

### HTTP 请求方式

> GET

### 支持格式

> JSON

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | author   | string   | RSA 二次加密后的用户信息                          |

</details>

<details>
<summary>14. 获取评论作者</summary>

### 接口功能

> 获取评论作者

### 权限要求

> su

### URL

> /api/v1/getAuthor/comment/<comment_id>

### HTTP 请求方式

> GET

### 支持格式

> JSON

### 请求参数

> | 参数  | 必选 | 类型   | 说明                               |
> | :---- | :--- | :----- | ---------------------------------- |
> | token | ture | string | 存放在 header 中<br>"token":"xxxx" |

### 返回字段

> | 返回字段 | 字段类型 | 说明                                              |
> | :------- | :------- | :------------------------------------------------ |
> | status   | string   | 返回结果状态<br>-success：正常 <br>-failure：错误 |
> | author   | string   | RSA 二次加密后的用户信息                          |

</details>
