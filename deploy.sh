for s in code web input
   do
      systemctl stop display_${s}.service 
      cp display_${s}.py /usr/bin/
      systemctl start display_${s}.service
      sleep 1
      systemctl status display_${s}.service
done 
