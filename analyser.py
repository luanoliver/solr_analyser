import numpy as np
import matplotlib.pyplot as plt
import pysolr
import json
import csv


def connect_to_solr(core, port=8983):
    solr_instance = pysolr.Solr('http://localhost:{}/solr/{}'.format(port, core), always_commit=True)
    return solr_instance


def search(solr_instance, query, n=100):
    result = solr_instance.search(query, **{'rows': n})
    return result


def read_csv(csv_file):
    csv_as_list = list()
    with open(csv_file) as f:
        csv_reader = csv.reader(f, delimiter=',')
        for line in csv_reader:
            csv_as_list.append(line)
    return csv_as_list


def is_relevant(result, csv_as_list):
    relevant = False
    c1, c2 = 0, 0
    for line in csv_as_list:
        if (result['key'] == line[0]):
            c1 += 1
            if (line[1] == '1'):
                relevant = True
                c2 += 1
        break
    print(c1, c2)
    return relevant


def main():
    query1 = 'Camera does not working with autofocus'
    query2 = 'The application is crashing after switching'
    relevancia_query1 = 'relevancia_q1.csv'
    relevancia_query2 = 'relevancia_q2.csv'
    solr = connect_to_solr('bolinha')
    r1 = read_csv(relevancia_query1)
    results = search(solr, query1)
    for r in results:
        check = is_relevant(r, r1)
        print(check)


if __name__ == "__main__":
    main()
