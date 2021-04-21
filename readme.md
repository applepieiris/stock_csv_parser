#该题为某量化公司的面试题：

输入： stock_price.csv
文件内保存了股票信息的价格信息：time,stock_id,exchange_id,price

实现功能： 每当股票价格上涨时（即某一个时刻的后一个时刻的价格高于当前时刻）在前一价格买入100股，计算每次买入之后30s，1min，5min（计算最近时间）可以赚到的钱

输出：time,stock_id,exchange_id,price,is_buy,r_30s,r_1min,r_3min,r_5min

工程文件说明：
reward_data.py 主功能实现代码
stock_price.csv 输入数据文件
stock_price_extended.csv 输出数据文件
