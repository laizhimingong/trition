# trition

版本：Python 3.8.2 Django==3.2.4 

项目背景：目前使用的普罗米修斯监控系统尚无告警可视化平台进行搜索、查询相关功能，必须打开不同url进行多层次点击才能查看告警，并且告警不能持久化存储数据库，无法实现回溯故障。

功能预期：

​	1.实现告警信息持久化存储

​	2.告警信息平台展示，并可进行查询

​	3.根据持久化告警信息，进行数据分析，并通过邮件形式固定周期发送告警情况

​	4.通过平台实现业务、组件、服务器等监控可视化与数据分析，掌握监控情况

​	5.支持平台自动化源数据接入：客户可自行定制监控内容（MySQL，redis，虚机服务，ES，windwos等）

​	6.支持定制开发运维操作

通过调用普罗米西斯监控系统Api,开发监控告警平台，一期主要实现报警信息收集展示、监控注册、服务数据分析，二期将构建监控自动化安装及面板构建
功能演示

![1](https://user-images.githubusercontent.com/44719269/167061430-ced21fb2-ddb3-41c5-9e6f-7a2716626ea9.png)
![10](https://user-images.githubusercontent.com/44719269/167061483-973cc2b2-170f-4528-9e2d-5a89abc6e4ec.png)
![7](https://user-images.githubusercontent.com/44719269/167061517-f59d4e23-e713-4b57-898d-436d1b53dff9.png)
![8](https://user-images.githubusercontent.com/44719269/167061535-09a382fc-5c42-4f72-a76d-f087b12aff9d.png)
![9](https://user-images.githubusercontent.com/44719269/167061551-0ce3fd2d-8007-405d-a536-e43fcdfa484e.png)
![11](https://user-images.githubusercontent.com/44719269/167061560-51be2730-d9da-4445-ad0f-1ae93fd0ba0f.png)
![12](https://user-images.githubusercontent.com/44719269/167061569-cfb3cbea-7001-4bb2-a32a-9c10bbbb109a.png)
![13](https://user-images.githubusercontent.com/44719269/167061576-0e25b887-017d-4260-bf78-4f446dd56dfe.png)
![14](https://user-images.githubusercontent.com/44719269/167061587-82987572-539e-4a5e-ae38-c2dceb5853a1.png)
![15](https://user-images.githubusercontent.com/44719269/167061594-2d723c73-7255-429d-a65e-afedf6595f7b.png)
![16](https://user-images.githubusercontent.com/44719269/167061612-6b95da7f-5f37-43ad-a3d5-40b7e5242244.png)
![17](https://user-images.githubusercontent.com/44719269/167061624-108524a5-339d-4cd9-9f6f-a47cbf55694e.png)
![18](https://user-images.githubusercontent.com/44719269/167061634-04f92e1b-03b8-4b0c-a637-d8a4a87c1993.png)
![2](https://user-images.githubusercontent.com/44719269/167061649-7186bb2e-ac51-4c0f-afc8-4749313fcc55.png)
![3](https://user-images.githubusercontent.com/44719269/167061662-3177de3c-453c-4787-9b64-8ff3c74d30e5.png)
![4](https://user-images.githubusercontent.com/44719269/167061671-7de0f247-053b-411c-8cd4-602f884c1ff4.png)
![5](https://user-images.githubusercontent.com/44719269/167061682-9d1798e6-3702-42e4-b2da-c9050eb4d4a6.png)
![6](https://user-images.githubusercontent.com/44719269/167061692-6419ff81-7bd0-4be5-829c-6d5fa5478756.png)

敏感信息已抹去
