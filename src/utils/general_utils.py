def humanise_passage(book, start_chapter, start_verse, end_chapter, end_verse):
    same_chapter = start_verse == end_chapter
    return "{book} {chapter} {rest}".format(
        book=book, chapter=start_chapter, rest=(
            "verse {start_verse}".format(start_verse=start_verse)
            if same_chapter and start_verse == end_verse
            else (
                "verses {start_verse} to {end_verse}".format(start_verse=start_verse,
                                                             end_verse=end_verse)
                if same_chapter
                else "verse {start_verse} to chapter {end_chapter} verse {end_verse}".format(
                    start_verse=start_verse, end_chapter=end_chapter, end_verse=end_verse)
            )
        )
    )
