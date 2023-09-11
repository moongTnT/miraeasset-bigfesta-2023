#!/bin/bash

# Anaconda 초기화 (Anaconda 설치 경로에 따라 변경 가능)
source ~/anaconda3/etc/profile.d/conda.sh

# 가상 환경 생성 및 활성화 (Python 버전 3.10.12로 설정)
conda create --name myenv python=3.10.12 -y
conda activate myenv

# requirements.txt가 있는 디렉토리로 이동
# cd /Users/mjkiim/Desktop/miraeasset-bigfesta-2023
cd {여기는_사용자_경로로}

# requirements.txt에 명시된 패키지 설치
pip install -r requirements.txt