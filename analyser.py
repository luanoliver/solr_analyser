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

def write_results(results, query):
    with open('{}.txt'.format(query), 'a') as file:
        file.truncate(0)
        for result in results:
            file.write('KEY: ' + result['key'] + '\n')
            file.write('SUMMARY: ' + result['summary'] + '\n')
            file.write('DESCRIPTION: ' + result['description'] + '\n')
            file.write('\n\n')

def is_relevant(result, csv_as_list):
    relevant = False
    for line in csv_as_list:
        if (result['key'] == line[0]):
            if (line[1] == '1'):
                relevant = True
            break
    return relevant


def main():
    count1, count2 = 0, 0
    query1 = 'Camera does not working with autofocus'
    query2 = 'The application is crashing after switching'
    relevancia_query1 = 'relevancia_q1.csv'
    relevancia_query2 = 'relevancia_q2.csv'
    solr = connect_to_solr('bolinha')
    r1 = read_csv(relevancia_query1)
    r2 = read_csv(relevancia_query2)
    results_q1 = search(solr, query1)
    write_results(results_q1, query1)
    results_q2 = search(solr, query2)
    write_results(results_q2, query2)
    print('QUANTIDADE DE RESULTADOS RETORNADOS DA Q1: {}'.format(len(results_q1)))

    print('-----RELEVANCIA Q1-----')
    for r in results_q1:
        check = is_relevant(r, r1)
        if check:
            count1 += 1

            print(r['key'])
    print('RESULTADOS RELEVANTES DA Q1: {}'.format(count1))
    print('QUANTIDADE DE RESULTADOS RETORNADOS DA Q2: {}'.format(len(results_q2)))
    print('-----RELEVANCIA Q2-----')
    for r in results_q2:
        check = is_relevant(r, r2)
        if check:
            count2 += 1

            print(r['key'])
    print('RESULTADOS RELEVANTES DA Q2: {}'.format(count2))

if __name__ == "__main__":
    main()
