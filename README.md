# nao_kinnect
Kinnect and Nao

Autorzy: Kamil Mówiński, Patryk Bogdański

 Freekinect:

      $ sudo apt-get install freenect
      $ sudo modprobe -r gscpa_kinect
      $ sudo modprobe -r gspca_main
      $ echo "blacklist gspca_kinect" |sudo tee -a /etc/modprobe.d/blacklist.conf

dodać użytkownika do grupy

      $ sudo adduser <nazwa_uzytkownika> plugdev
      
sprawdzenie działania

      $ freenect-glview

Powinno wyświetlić się okienko z widokiem z kamery normalnej i z kamery głębi (czasami występują błędy ale nie wpływają na dalszą cześć, np. nie wyświetla się okno ale wykrywa urządzenia).

UWAGA!
Jak nie znajduję urządzenia trzeba podłączyć go do innego portu USB (działa na USB 2, na USB 3 są problemy)


Środowisko ROS

       $ source /opt/ros/hydro/setup.bash
       $ mkdir -p ~/catkin_ws/src
       $ cd ~/catkin_ws/src
       $ catkin_init_workspace
       $ cd ~/catkin_ws/
       $ catkin_make
       $ source devel/setup.bash
       $ sudo apt-get install ros-hydro-openni-camera
       $ sudo apt-get install ros-hydro-openni-launch
       $ sudo apt-get install ros-hydro-openni-tracker

Ze strony pobieramy oprogramowanie NITE dla openi
www.openni.ru/openni-sdk/openni-sdk-history-2/

Pobrieramy plik i rozpakowujemy go
NiTE v1.5.2.23

następnie instalujemy jako administrator (w folderze gdzie rozpakowaliśmy NiTE):

        $ ./install.sh

Podgląd 
Będąc w środowisku catkin (source ~/catkin_ws/devel/setup.bash), wpisujemy każdą komendę w innym temrinalu

        $ roslaunch my_kinnect kinnect.launch

Aby wyświetlić szkielet układy współrzędnych w rviz należy (lub wykorzystać plik coords.rviz):
-Kliknąć przycisk "Add"
-W okienku wybrać "TF" i zatwierdzic
-W zakładce "Global Options" w polu "Fixed Frame" wpisac "openni_depth_frame" (lub wybrać jeśli jest)

Aby rviz wykrył poprawnie wszystkie "tematy" (topic) konieczna jest kalibracja (ręcę pod kątem prostym w odpowiedniej odległości).



Dalsze przetwarzanie:
Dane o położeniach użytkownika są dostępne jako transformy o nazwach head_1, torso_1, torso_2 itp...
Maksymalnie można przechowywać dane o 3 użytkownikach (http://wiki.ros.org/openni_tracker).


Skrypt który publikuje informację o przetworzeniu (głowa):

       $ rosrun my_kinnect tracker.py 

Pozostałe części ciała

       $ rosrun my_kinnect tracker.py _target_joint:=/left_hand

Naoqi SDK
1. rozpakować archiwum w docelowe miejsce
2. dodać do pliku ~/.bashrc

      export PYTHONPATH=${PYTHONPATH}:/path/to/python-sdk

3. zrestartować powłokę.
