import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Path To PDF')
    parser.add_argument('dilution', help='Integer between 3-8 -> 6 gives good results', type=int)
    parser.add_argument('image', help='original or diluted')
    args = parser.parse_args()
    
    from picasso.document import Document
    from picasso.page2yolo import write_xml

    from progressbar import progressbar

  
    print("Starting with Parameters:")
    print(args)

    d = Document(args.file)
    d.process(args.dilution)

    save_to_path = 'source_images'

    for page in progressbar(d.pages):
        # Save either the original image or the diluted one
        if args.image == 'original':
            filename = page.save(save_to_path)
        elif args.image == 'diluted':
            filename = page.save_diluted(save_to_path)

        # Save images with bboxes for further manual filtering
        write_xml(page, filename, folder=save_to_path)

