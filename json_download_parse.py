import json
import urllib.request
import shutil
import os
import time
import heroes
import pprint
import sys

def GetFileName(match_id):
	match_file_name = match_id + '.json'
	return match_file_name

def DownloadMatchData(match_id, verify=True):
	match_file_name = GetFileName(match_id)
	download = True
	if verify is True:
		if os.path.isfile(match_file_name) is True:
			download = False
		
	if download is True:
		url = 'https://api.opendota.com/api/matches/'
		full_url = url + match_id
		with urllib.request.urlopen(full_url) as url_stream, \
			open(match_file_name, 'wb') as download_file:
				shutil.copyfileobj(url_stream, download_file)
		time.sleep(0.5)


def ParseMatchData(match_id):
	with open(GetFileName(match_id), encoding="utf8") as data_file:    
		data = json.load(data_file)
	return data

def DownloadAndParse(match_id, verify=True):
	DownloadMatchData(match_id=match_id, verify=verify)
	return ParseMatchData(match_id)

	
def PatchVerification(pro_match_batch, patch):
	with open(pro_match_batch, encoding="utf-8") as data_file:
		pro_match_data = json.load(data_file)
		
	match_data = []
	oldest_match_id = 0
	continue_downloading = True
	for i in range(0,100):
		match_data.append(DownloadAndParse(str(pro_match_data[i]['match_id'])))
		
		if match_data[i]['patch'] != patch:
			last_good_match_id = i-1 # ID w PĘTLI
			oldest_match_id = match_data[last_good_match_id]['match_id'] #ID GRY
			continue_downloading = False
			break
	
	if continue_downloading is True:
		oldest_match_id = match_data[99]['match_id']
		
	return (oldest_match_id, continue_downloading)
	
def GetPickListByMatchID(match_id):
	RadiantPicks = []
	DirePicks = []
	MatchData = DownloadAndParse(match_id)
	for i in range(0,5):
		RadiantPicks.append(MatchData['players'][i]['hero_id'])
	for i in range(5,10):
		DirePicks.append(MatchData['players'][i]['hero_id'])
	
	return DOTA_Heroes.GeneratePickList(RadiantPicks, DirePicks)
	
if __name__ == '__main__':
	DOTA_Heroes = heroes.DOTA_Heroes()

                    
        






        