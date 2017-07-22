注意事項
--------------
*   提供樹梅派Linux的映像檔：[點我下載](https://drive.google.com/file/d/0BzKhDssP3107TlhXTDJ5LTRwUnc/view?usp=sharing)
*   提供映像檔燒錄軟體(windows版本[點我下載](https://drive.google.com/file/d/0BzKhDssP3107WVkyQ3JiTkZvSWM/view?usp=sharing))，Linux可以透過dd來完成
*   請注意！！登入帳號為：`pi`，登入密碼：`raspberrypi`，root無密碼，`sudo su`直接enter即可
*   執行範例程式方式為
```
cd olami
sudo ./startup.sh
```


*   提供聲音調整command, 底下為將音量調整成到最大
```
sudo cp vol /usr/local/bin
sudo chmod a+x /usr/local/bin/vol
vol 100
```
*   Use the vol script like so:
```
vol     # Outputs the current volume as a number between 0 and 100
vol +   # Turn up the volume by 3
vol -   # Turn down the volume by 3
vol 85  # Set the volume to 85
```
