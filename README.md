# getRefs

从各种形式的参考文献引用，下载供 Endnote 导入的引用格式。

## 安装

```bash
# 获得代码
git clone https://github.com/Metaphorme/getRefs.git
cd getRefs

# 安装 ChromeDrive
# 从这里下载适合的版本：https://chromedriver.chromium.org/downloads
# 将 ChromeDrive 下载到当前目录即可。当前目录已被加入环境变量。

# 安装依赖
pip3 install -r requirements.txt
```

## 使用

```bash
# 创建需要引用的论文集
touch refs.txt

# 向其中加入需要引用的论文，每行一个
# 格式随意，只要 Google 能看懂就行
# refs-example.txt 是一个示例，它的内容如下：
[22] Zhang, B., Li, M., McDonald, T., Holyoake, T. L., Moon, R. T., Campana, D., Shultz, L., & Bhatia, R. (2013). Microenvironmental protection of CML stem and progenitor cells from tyrosine kinase inhibitors through N-cadherin and Wnt-β-catenin signaling. Blood, 121(10), 1824–1838. https://doi.org/10.1182/blood-2012-02-412890
[23] Quintás-Cardama, A., & Cortes, J. (2009). Molecular biology of bcr-abl1-positive chronic myeloid leukemia. Blood, 113(8), 1619–1630. https://doi.org/10.1182/blood-2008-03-144790

# 你需要在 getEndnote.py 的 PROXY 项目设置代理

# 开始查询
./getEndnote.py

# enw 文件会下载到 enws 文件夹内
```

## 已知错误

1. 在处理搜索不到的文献时会卡死
2. 文献可能下载重复

## 常见问题

Q：为什么出现了无法定位的情况？

A：网页布局有变，可能需要自行修改下 browser.find_element(By.XPATH, ...) 的内容。

Q：为什么有这么多 bug 还发出来？

A：考试周写的，有 bug 没时间修。

Q：可不可以实现 xxx 功能？

A：PR welcome！

**如果这个小工具可以帮到你，请帮我点个小星星🌟吧！**

