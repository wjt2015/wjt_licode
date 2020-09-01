#!/bin/sh
echo "开始安装licode的依赖:"
./scripts/installMacDeps.sh

echo "开始安装licode:"
./scripts/installErizo.sh
./scripts/installNuve.sh  

echo "安装example:"
./scripts/installBasicExample.sh  

echo "初始化licode组件:"
./licode/scripts/initLicode.sh

echo "初始化example:"
./scripts/initBasicExample.sh  

echo "完成!"













