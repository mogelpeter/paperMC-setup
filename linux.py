import io
import subprocess
import os
import json
import platform

def load_server_properties():
    min_ram = "1G"
    max_ram = "2G"
    if os.path.exists("server.properties"):
        with open("server.properties", "r") as f:
            for line in f:
                if line.startswith("min_ram_gb="):
                    min_ram = line.strip().split("=")[1] + "G"
                elif line.startswith("max_ram_gb="):
                    max_ram = line.strip().split("=")[1] + "G"
    return min_ram, max_ram

def get_minecraft_version():
    if os.path.exists("version_history.json"):
        with open("version_history.json", "r") as f:
            data = json.load(f)
            return data.get("currentVersion", "Unknown")
    return "Unknown"

def find_java_path():
    java_path = ""
    try:
        java_path = subprocess.check_output(["which", "java"]).decode("utf-8").strip()
        java_path = os.path.dirname(java_path)
    except subprocess.CalledProcessError:
        print("Java not found in the system PATH.")
    return java_path

def create_start_script(min_ram, max_ram, java_dir):
    start_script = f"""
#!/bin/sh
server_name="server"
join_screen=true
jar_file="paper.jar" # server core file
min_memory="{min_ram}"
max_memory="{max_ram}"
server_port="" # std - 25565
force_chunks_upgrade=false

java_dir="{java_dir}"
profiling=false # JDK profiling (reduces performance)
fix_java_12_issues=false
debugging_port="" # if none - debugging is off
log4j_config="" # log4j settings file

# DO NOT CHANGE src: https://mcflags.emc.gs
aikar_jvm_flags="-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true"
jvm_flags="-server -Dfile.encoding=UTF-8"
app_flags="nogui"
screen_name="${{server_name}}"
htop_name="${{server_name}}"
script_name=`basename "$0"`

if [ "$1" != "screen" ]; then
    screen -A -m -d -S ${{screen_name}} bash ${{script_name}} screen
    [ "$join_screen" = true ] && screen -x ${{screen_name}}
    exit
fi

if [ "$java_dir" != "" ]; then
    java_cmd="${{java_dir}}/java"
else
    java_cmd="java"
fi

jvm_flags="${{jvm_flags}} ${{aikar_jvm_flags}}"
if [ "$profiling" = true ]; then
    htop_name="${{htop_name}}-profiling"
    jvm_flags="${{jvm_flags// -XX:+PerfDisableSharedMem/}}"
    jvm_flags="${{jvm_flags}} -Xshare:off"
fi
htop_name="$USER.${{htop_name}}"

[ "$fix_java_12_issues" = true ] && jvm_flags="${{jvm_flags}} --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.lang.reflect=ALL-UNNAMED --add-opens java.base/java.lang.invoke=ALL-UNNAMED --add-opens java.base/java.security=ALL-UNNAMED"
[ "$debugging_port" != "" ] && jvm_flags="${{jvm_flags}} -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=0.0.0.0:${{debugging_port}}"
[ "$log4j_config" != "" ] && jvm_flags="${{jvm_flags}} -Dlog4j.configurationFile=${{log4j_config}}"

[ "$server_port" != "" ] && app_flags="${{app_flags}} -port ${{server_port}}"
[ "$force_chunks_upgrade" = true ] && app_flags="${{app_flags}} --forceUpgrade"

jvm_flags="-D_server=${{htop_name}} -Xms${{min_memory}} -Xmx${{max_memory}} ${{jvm_flags}}"

while true
do
    eval $java_cmd ${{jvm_flags}} -jar ${{jar_file}} ${{app_flags}}
    echo "Server ${{screen_name}} stopped. Rebooting in:"
    for i in {{3..1}}
    do
        echo "$i..."
        sleep 1
    done
done
"""
    return start_script

def start_server():
    min_ram, max_ram = load_server_properties()
    java_dir = find_java_path()
    start_script = create_start_script(min_ram, max_ram, java_dir)
    script_file = "start_temp.sh"
    with open(script_file, "w") as f:
        f.write(start_script)
    os.chmod(script_file, 0o755)
    process = subprocess.Popen(['bash', script_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Server started...")
    for line in io.TextIOWrapper(process.stdout, encoding='utf-8', errors='replace'):
        print(line, end='')

if __name__ == "__main__":
    start_server()
