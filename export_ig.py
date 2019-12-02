import basic
from pandas import DataFrame
import sys

sql = "SELECT id,comments_disabled,typename,id_ig,media_to_caption, shortcode,media_to_comment_count," \
      "taken_at,display_url,liked_by_count,media_preview_like_count,id_owner," \
      "is_video,view_video_count,accessibility_caption FROM ig_read_json WHERE params_query = '"

# ORDER BY id"

id = []
comments_disabled = []
typename = []
id_ig = []
media_to_caption = []
shortcode = []
media_to_comment_count = []
taken_at = []
display_url = []
liked_by_count = []
media_preview_like_count = []
id_owner = []
is_video = []
view_video_count = []
accessibility_caption = []

if __name__ == '__main__':
    params_query = sys.argv[1]

    fileCsvName = params_query+"_ig_posts.csv"
    try:
        mypointer = basic.cnx.cursor()
        mypointer.execute(sql + params_query + "' ORDER BY id ASC")
        records = mypointer.fetchall()

        for row in records:
            id.append(row[0])
            comments_disabled.append(row[1])
            typename.append(row[2])
            id_ig.append(row[3])
            media_to_caption.append(row[4])
            shortcode.append(row[5])
            media_to_comment_count.append(row[6])
            taken_at.append(row[7])
            display_url.append(row[8])
            liked_by_count.append(row[9])
            media_preview_like_count.append(row[10])
            id_owner.append(row[11])
            is_video.append(row[12])
            view_video_count.append(row[13])
            accessibility_caption.append(row[14])

            Igcsv = {'id': id, 'comments_disabled': comments_disabled, 'typename' : typename,
                     'id_ig' : id_ig, 'media_to_caption':media_to_caption,'shortcode':shortcode,
                     'media_to_comment_count':media_to_comment_count,'taken_at':taken_at,'display_url':display_url,
                     'liked_by_count':liked_by_count,'media_preview_like_count':media_preview_like_count,
                     'id_owner':id_owner,'is_video':is_video,'view_video_count':view_video_count,
                     'accessibility_caption':accessibility_caption}

            ig_cols = ['id','comments_disabled','typename','id_ig','media_to_caption','shortcode',
                       'media_to_comment_count','taken_at','display_url','liked_by_count','media_preview_like_count',
                       'id_owner','is_video','view_video_count','accessibility_caption']

        df = DataFrame(Igcsv,columns = ig_cols)
        export_csv = df.to_csv(fileCsvName,index=None,header=True)
        print(df)

    except basic.Error as e:
        print("Error MySQL di: ", e)