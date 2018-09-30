import json
with open('Constructin-Helmet Bounding.json', 'r') as f:
	read_data = f.readlines()

my_list = []
for c in read_data:
	my_list.append(json.loads(c))
for image in my_list:
	imageFile = image['content'].split('/')[-1].split('___')[-1].split('.')[0] + '.txt'
	print(imageFile.split('.')[0]+'.txt')
	for label in image['annotation']:
		m = ('%s\n%s %s %s %s' % (
				0,
				int(label['points'][0][0] * label['imageWidth']),
				int(label['points'][1][1] * label['imageHeight']),
				int(label['points'][2][0] *  label['imageWidth']),
				int(label['points'][2][1] * label['imageHeight'])
				))
		print(m)
	with open('C:\\Users\\Gabriela\\Documents\\Gabriel\\Labels\\'+imageFile, 'w') as f:
		f.write(m)
	
