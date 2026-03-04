@echo off
echo =========================================
echo Iniciando o Robo do Boleto da Impacta...
echo =========================================

D:

cd "D:\Projetos\automacaoBoleto\automacao-boleto"

call venv\Scripts\activate

python main.py

pause