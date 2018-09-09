## 航班数据可视化

### 数据

数据来源：

- 静态本地数据集：https://openflights.org/data.html
- 爬虫爬取：http://www.variflight.com/

### 设计

- 结构梗概：爬虫——数据——Echarts可视化， 前期工作通过Python完成，可视化使用JavaScript、HTML以及Echarts框架完成
- 爬虫：
  - http://www.variflight.com 的查询网址格式为："http://www.variflight.com/flight/" + departure airport IATA code + "-" + arrival airport IATA code + ".html?AE71649A58c77&fdate=" + date
  - 使用lxml库以及XPath解析网页，获取航班数据，得到公司名称、航班号、计划起飞以及计划到达时间、起始地以及到达地、查询时该航班的状态
  - 由于该网站对实际起降时间做出了反爬虫处理——以临时图片的形式加载，这导致了无法通过OCR技术直接获得该航班实际起降时间，只能通过另一种方式获取实际起降时间：通过访问该航班查询结果所指向的页面，获取延迟时间以及飞行时间计算出实际起降时间
  - 通过以上途径获取某天某条航线的所有航班信息后，通过pymysql库将结果存储到mysql中
  - 不足：反反爬虫还没有做到位，导致爬取速度有限，目前只能爬取一条航班的数据
- 数据存储：
  - 在存储数据之前，通过Python将原始数据处理成需要的数据，并格式化地将数据存到JSON、CSV或mysql中(依用途而定)
  - 由于还不会搭建本地服务器，JavaScript读取JSON数据只能通过取巧的方式进行：用Python存储数据时，在生成JSON数据外，还将其改存为`var name = 'JSON';`的形式存在.js文件里，相当于直接生成一个变量， 将.js文件引入即可使用吗 
  - CSV和mysql的数据通过Python的pandas module 和 pymysql module进行交互。
- 数据可视化：
  - 初步观察、分析数据，确定需要展现的数据
  - 通过Echarts框架，将需要展现的数据进行动态可视化处理并通过HTML展现。
  - 通过动态可视化处理，可以更好地展现本次所选的数据的特性，尤其是针对时间序列数据

### 功能

- 鉴于本次作品的特殊性，根目录下的两个.html文件就是最终成果
- 由于技术原因，不能实现完全的自动化流程，一些操作需要直接通过修改源码进行
- 首先需要确定爬取的航线的出发机场IATA码，到达机场IATA码，日期(YYYYMMDD格式， 整型)，在命令行以`$ python spider.py departureAirportIATA arrivalAirportIATA date`的格式运行spider.py文件，等待执行完毕后所查询的航班数据就会存放mysql数据库里
- 之后需要修改cal_realtime.py文件里的数据处理函数
  - 依照已有的函数格式，手动写函数，因为不同的feature对应的数据处理方式略有不一样，特别是sql的查询语句
  - 将数据分析的结果以`var name = 'JSON';`格式化存在.js文件里, 其中JSON部分的格式是：
    - `{date1:[{name:str, value:int}, ..], ..} `
  - 因为算法原因，需要手动修改一下生成的.js文件，将`[{name:str, value:int}, ..]`中行末的逗号以及`{date1:[{name:str, value:int}, ..], ..} `最后一个list后面的逗号都删掉
- 最后通过配置根目录下的realtime.html 文件 以及JavaScripts文件夹中的realtime.js，获得可视化界面
- 通过可视化界面可以直观地看出数据中隐藏的信息。
- **注1： 可能需要修改源文件中的mysql密码才能在别的电脑上正确执行数据库相关的程序！**
- 注2：由于爬虫爬下来的数据存在本地mysql数据库中，若要查看数据，则需要使用data目录下的information.sql文件导入数据对其进行查看 
- 注2：开启win10的颜色滤镜中的红-绿(红色弱, 红色盲)滤镜，对可视化界面的色彩的体验更佳

### 后续计划

- 加强反反爬虫功能，使用IP代理伪装，以便更快速地获取数据，提高查询效率，并且获得更多数据以支持更多数据分析维度
- 搭建动态页面，将上述所有功能通过自动化处理使得已有的可视化图表每天自动更新(由于无需修改图表以及数据的存储结构、查询方式，因此没有涉及必须修改源代码的部分)
- 添加查询功能以及利用机器学习实现航班延误预测功能



**Appendix**:

​	Python依赖库：bs4, urllib, pandas, numpy, lxml, re, time, pymysql, sys

​	JavaScript: Echarts, Echarts_GL