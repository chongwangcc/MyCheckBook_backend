
# 记账本后台

## 1.软件功能
本项目主要为记账本后台程序、提供对应的restful接口，以及web后台管理系统。
记账本项目主要功能是记账，出每月财报，以及对某些关键指标的可视化展示

## 2. 安装环境、启动命令
环境
- Python3.6

打包工程：
```
python setup.py sdist --dist-dir _bin
```
或者
```
python setup.py bdist_wheel --dist-dir _bin
```

安装依赖命令：
```
pip install -r requirements.txt
```

启动命令：
```
cd mycheckbook_backend
python3 app.py
```

打开网址: ```http://<IP>:9002/login```， 如下图：

![avatar](./_doc/login.PNG)

![avatar](./_doc/every_day_sum.PNG)


## 3. 使用说明


## 4. 代码目录结构说明
```

```

## 5. 常见问题


## 6. 后续开发计划
