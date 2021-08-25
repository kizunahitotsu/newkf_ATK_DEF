测试一下效果（

# 使用说明：
0. 确保已安装python最新版本，非最新版本不一定兼容
1. 将最新版本的计算器解压放入'代码'文件夹中，选择覆盖即可
    + 程序会自行填写newkf.in
2. 按以下填写规范填写option.txt
3. 运行迭代.bat，即可进行迭代
    + 若报错，请按报错信息或填写规范检查option.txt
    + 若检查无误后仍然报错，请联系作者，可能是该修BUG或者更新了（
4. 迭代可在中途关闭程序，重新运行程序会从当前轮次迭代重新开始
5. 若完成一次迭代，可运行 #待填写 .bat，即可生成'记录（日期）'文件夹，包含迭代记录，同时迭代信息会初始化，可直接进行新的一次迭代
___
# option.txt填写规范：
## （虽然会兼容各种奇怪的填写姿势，但为避免报错还请按格式填写）
+ calculation部分请在'='后填入适当范围内的数字，范围详见计算器贴
+ iteration部分请在'='后填入适当范围内的数字或'ON'、'OFF'
    + pool recording为是否记录迭代的PC结果
    + ATK/DEF mode为分攻守迭代模式
    + cycle mode为循环迭代模式，优点为收敛速度更快，缺点为难以对迭代结果进行控制变量的定性研究，请视需求选择是否开启
+ gear filter部分请在'='后填入0或1，其中0为不屏蔽，1为屏蔽，神秘装备同理；支持新增装备，直接按格式填入即可，注意保证神秘装备包含在普通装备里
+ aura filter部分请直接填入需要屏蔽的天赋，并用空格、换行或'_'分隔
+ role filter部分请在'='后填入需要屏蔽的装备、神秘装备和天赋（不屏蔽则不填，或填入NONE），并用空格、换行或'_'分隔；支持新增角色，直接按格式填入即可
+ group部分请设置每组的组名（形如group_Leek，仅支持 #待填写 ）、光环、卡片、装备、许愿池、护符（支持换行）、装备、神秘装备（若不使用神秘装备，请将最后的1改成0）、该组PC个数
