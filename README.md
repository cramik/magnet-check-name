# magnet-check-name

Given a set of torrent magnet uris and a tracker list waits for metadata and outputs in the form (info-hash,"name"). Good for naming a large set of unsorted/unnamed magnet links

Hard-coded inputs:
- magnets.txt (magnet uris seperated by newline)
- trackers.txt (tracker urls seperated by newline) [https://github.com/ngosang/trackerslist]
