import libtorrent as lt
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

ses = lt.session()
params = {
    'save_path': '/dev/null', #libtorrent doesnt appear to work Windows so this is not a risk of platform dependancy
    'storage_mode': lt.storage_mode_t(2),
    'file_priorities': [0]*5, #dont_download{0}
}

# Creates handles for every magnet link
handles = []
with open("magnets.txt",'r') as magnets:
    for i,magnet in enumerate(set(magnets)):
        magnet = magnet.strip()
        try:
            t = lt.add_magnet_uri(ses, magnet, params)
            if(t not in [handle[1] for handle in handles]): # Check we got a unique handle back to prevent dupe in handles array
                t.set_download_limit(0)
                handles.append((magnet,t))
        except:
            print(f"Error adding magnet - {magnet} on line {i}")
            pass

#Add trackers for each magnet
with open("trackers.txt") as trackers:
    for tracker in trackers:
        for handle in handles:
            if(tracker.strip()!=''): #Ignore empty lines since some lists have them
                handle[1].add_tracker({"url": tracker.strip()})

#Check for torrent names every 1 second until no torrents left, if name exists remove torrent
while (len(handles)!=0):
    for handle in handles:
        try:
            if(handle[1].has_metadata()):
                print(f"{handle[1].info_hash()},\"{handle[1].name()}\"")
                ses.remove_torrent(handle[1])
                handles.remove(handle)
        except:
            print(f"Error occured on torrent with magnet {handle[0]}")
    time.sleep(1)
