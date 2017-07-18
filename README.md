# kervice
基于redis 的微服务新模式

本项目需要python3环境，建议安装[miniconda3](https://conda.io/miniconda.html)
最好用pyenv管理你的python版本

## 初始化本项目，首先需要安装fabric

```
# python3 安装fabric会报错，所以安装fabric3就好了
pip install fabric3
```

## 初始化相关工具

```
pipreqs 用于生成 requirements.txt 文件
ujson python中最好的json解析模块
click Python命令行神器
sanic web框架
Sanic-Cors k跨域处理
AoikLiveReload 热加载
```