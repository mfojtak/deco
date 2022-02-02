import glob
import gzip
import os
import nltk.data
nltk.download('punkt')
from lxml import html
from dask.distributed import Client, progress, Lock, as_completed


def xml_loader(file):
    et = html.parse(file)
    root = et.getroot()
    articles = root.xpath("//medlinecitation")
    for article in articles:
        id = int(article.xpath("pmid")[0].text_content())
        abstract = article.xpath("article/abstract")
        if abstract:
            text = str(abstract[0].text_content()).replace("\n", " ").replace("\t", " ")
        else:
            continue
        #authors = child.find("MedlineCitation/Article/AuthorList")
        #if authors is not None:
        #    for author in authors:
        #        author_str = "{} {}".format(author.find("ForeName").text, author.find("LastName").text)
        yield {"text": text}

tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
archive_path = "/data/pubmed/abstracts"


def chunks(elements, n):
    batch = []
    for element in elements:
        batch.append(element)
        if len(batch) >= n:
            yield batch
            batch.clear()
    if batch:
        yield batch


def process_batch(batch, no):
    with open("{}/{}.tsv".format(archive_path, no), 'w') as textfile:
        for file in batch:
            with gzip.open(file, 'rb') as gz:
                for article in xml_loader(gz):
                    sents = tokenizer.tokenize(article["text"])
                    for sent in sents:
                        textfile.write(sent.strip() + "\n")
                    textfile.write("\n")


def build_archive(client):
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    files = glob.iglob("/data/pubmed/ftp.ncbi.nlm.nih.gov/pubmed/baseline/*.xml.gz", recursive=True)
    futures = []
    for index, chunk in enumerate(chunks(files, 1)):
        future = client.submit(process_batch, chunk, index)
        futures.append(future)
    progress(futures)


if __name__ == '__main__':
    #cluster = KubeCluster.from_yaml('worker-spec.yaml')
    #cluster.adapt(minimum=16, maximum=20)
    client = Client()
    build_archive(client)
