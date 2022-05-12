# newkf ATK/DEF 咕咕镇迭代器v3.2
## 关于迭代器
+ 本迭代器使用迭代算点的方法，模拟咕咕镇某一pvp环境中的最优反应，以此逼近纳什均衡。
+ 迭代器能够一定程度上（取决于模拟精度）算出一定条件下的优势流派，及其克制关系。
+ 作为代价，迭代器的运行时间通常以10小时甚至天为单位。
### 关于分攻守
+ 迭代器会根据配置信息将所有PC分为`ATK`、`DEF`、`MIX`共3大组。
+ `ATK`组以`DEF`组和`MIX`组为对手进行`DEFENDER 0`算点。
+ `DEF`组以`ATK`组和`MIX`组为对手进行`DEFENDER 1`算点。
+ `MIX`组以所有PC为对手进行`DEFENDER 2`算点。
+ 请确保`MIX`组非空，或`ATK`组和`DEF`组均非空。

## 使用说明
### 准备
1. 本程序在Python3.9下测试运行。请确保Python的版本至少为3.8（估计）以上。
    + 如需使用导出计算结果至Excel的功能，请安装openpyxl库：`pip install openpyxl`
2. 将最新版本的[计算器](https://bbs.9shenmi.com/read.php?fid=86&tid=807309&sf=407)放入`\代码`文件夹。
    + 截至目前为`0.4.0.1`版，对应咕咕镇`2022/05/11`版本。
    + 若有更新角色/装备/光环，请在`\代码\lib.txt`按照格式更新相应信息。
3. 按照格式填写`option.txt`。具体如下：
    + `[Calculation]`部分
        + `Threads`：计算器中的THREADS。
        + `Tests`：计算apc时，计算器中的TESTS。
        + `Seedmax`：计算器中的SEEDMAX。
        + `Verbose`：计算器中的VERBOSE。
        + `Tests_vb`：计算vb时，计算器中的TESTS。
    + `[Iteration]`部分
        + `Turns`：需要进行迭代的轮数。
        + `ATK/DEF mode`：目前不起作用。后续更新可能会设计为可开关的模式。
    + `[Gear]`部分
        + `=`后面填入`1`或`0`。1为使用该普通装备，0为不使用。
    + `[Myst]`部分
        + `=`后面填入`1`或`0`。1为使用该神秘装备，0为不使用。
    + `[Aura]`部分
        + `=`后面填入`1`或`0`。1为使用该光环，0为不使用。
    + `[Role]`部分
        + 格式为：`<Role>={<Gear1> <Gear2>;<Myst1> <Myst2>;<Aura1> <Aura2>}`
        + 所填入为计算该角色时额外**屏蔽**的普通装备/神秘装备/光环。
        + 注意分隔符，若不需要屏蔽请留空。
    + `[Group]`部分
        + `Name`：组名。
        + `Defender`：计算器中的DEFENDER。
        + `Size`：该组最大PC个数。若超过`Size`，将会进行淘汰，保留胜率最高的`Size`个。
        + `Aura value`：该组的光环值。
        + `Card`：该组的卡片信息。
        + `Wish`：该组的许愿池信息。可以留空。
        + `Amulet`：该组的护符信息。可以留空。
        + `Gear`：该组的普通装备信息。
        + `Myst`：该组的神秘装备信息。
    + 注意没有写检查`option.txt`格式的功能。请务必严格按照格式填写。
### 迭代
1. 开始一轮新的迭代
    + 移除或清空`\记录`文件夹。一般建议重命名。
    + 运行`iterate.py`。
2. 暂停迭代
    + 直接停止运行`iterate.py`即可。
3. 继续迭代
    + 直接运行`iterate.py`即可。
    + 会从上次终止的轮数开始。
### 导出Excel
1. 运行`statistics.py`
2. 输入需要统计的文件夹名，默认为`记录`。
3. 输入需要统计的轮数范围。
4. 输入导出的表格名，默认为`统计结果.xlsx`。

## 更新日志
### v3.1
+ 添加对`WU`的支持，目前按0成长值处理。
### v3.2
+ 添加对`XI`的支持，目前按0成长值处理。

## 更新计划
+ 加入对成长值的支持，目前还没想好怎么实现。
+ 加入GUI，主要用于填写`option.txt`，避免手动填写格式出错。
+ 加入自定义分组（角色，装备，神秘装备，光环，MAXATTR）的功能。可以排除不可能的组合，加快计算速度。
+ 与胜率计算器组合，得出PC两两之间的胜率。
+ 加入更多可选的淘汰模式、装备选择模式。
+ 加入自定义PC权重。

## 鸣谢
kf@brutelor
