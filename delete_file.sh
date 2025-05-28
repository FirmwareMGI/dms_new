for f in /home/pi/dms/DMSv1.2/IEC61850/DR_FILES/* .*; do
  [ -f "$f" ] && printf "%s " $(perl -e 'print((stat("$ARGV[0]"))[9])' -- "$f") && \
  printf "%s\0" "$f";
done | tr '\0\n' '\n\0' | sort -k1nr | \
sed "1,20d;s/'/'\"'\"'/g;s/[^ ]* \(.*\)/rm -f -- '\1';/" | tr '\0' '\n' | sh
