# Exercise #9. Python Programming

import numpy as np
import matplotlib.pyplot as plt

#########################################
# Question A1 - do not delete this comment
#########################################

def analyze_rating_data (filename):
    rating = np.loadtxt(filename,delimiter=',')

    # The number of seasons (number of rows in the table)
    print ('The number of seasons:')
    print (len(rating))

    # The highest rating recorded in the entire file for an episode (maximum value in the table)
    print ('The highest rating ever recorded for an episode:')
    print (rating.max())

    # Average rating for the first episode over all seasons (average of the first column)
    print ('Average rating for the first episode over all seasons:')
    print (np.mean(rating[:,0]))

    # Number of episodes which had a rating lower than 8 (how many values lower than 8 exist in the table)
    print ('Number of episodes which had a rating lower than 8:')
    print (np.sum(rating < 8))

    # Is there at least one episode with a rating of 15 ? Print True or False without using IF
    print ('Is there at least one episode with a rating of 15:')
    print (np.any(rating == 15))

    # What is the maximal total season rating ? (sum the rating in each season and print the maximum over the sums)
    print ('The maximal total season rating:')
    print (np.max(rating.sum(axis=1)))

    # Print a vector holding the minimal rating for each episode (vector of column minimums)
    print ('Minimal rating for each episode:')
    print (rating.min(axis=0))

#Testing your code -------------------------------
print ('Output for ISRAEL:----------------------')
analyze_rating_data('Israel.csv')
print ('Output for SPAIN:-----------------------')
analyze_rating_data('Spain.csv')


#########################################
# Question B1 - do not delete this comment
#########################################
def load_covid_world_matrix(filename, fieldname):
    countries_dic = {}
    dates_lst = []
    matrix = []
    fr = None
    try:
        fr = open(filename, 'r')
        fieldlst = fr.readline().strip('\n').split(',')
        fieldindex = 0
        for f in fieldlst:  ## find the index of fieldname
            if f == fieldname:
                break
            else:
                fieldindex += 1

        for line in fr:
            tokens = line.strip('\n').split(',')
            date = tokens[3]
            country = tokens[2]
            if country == 'International' or country == 'World':
                continue
            if country not in countries_dic:
                countries_dic[country] = {}
                if tokens[fieldindex] == '':
                    countries_dic[country][date] = 0
                else:
                    countries_dic[country][date] = float(tokens[fieldindex])
            else:
                if tokens[fieldindex] == '':
                    countries_dic[country][date] = 0
                else:
                    countries_dic[country][date] = float(tokens[fieldindex])
            if date not in dates_lst:
                dates_lst.append(date)

        countries_lst = countries_dic.keys()

        for country in sorted(countries_lst):
            country_data = []
            v = countries_dic[country]
            for date in sorted(dates_lst):
                country_data.append(v.get(date,0))
            matrix.append(country_data)
    except IOError:
        print('IOError encountered')
    finally:
        if fr != None:
            fr.close()
        return np.array(sorted(countries_lst)), np.array(sorted(dates_lst)), np.array(matrix)


#########################################
# Question B2 - do not delete this comment
#########################################
def analyze_covid_data(countries, dates, matrix):
    print ('Are there any negative values in the table?')
    print ((matrix < 0).any())

    print ('In how many days more than 8000 new cases were identified in Israel?')
    print ((matrix[countries == 'Israel'] > 8000).sum())

    print ('Number of countries with more than 1 million total cases:')
    print (np.sum(np.sum(matrix,axis=1)>1000000))

    print ('Name of country with the highest total number of daily cases in the first 30 days appearing in the table:')
    print (countries[np.argmax(matrix[:,:30].sum(axis = 1))])

    print ('Date with maximal number of new cases in all countries together:')
    print (dates[np.argmax(matrix.sum(axis=0))])



#########################################
# Question B3.1 - do not delete this comment
#########################################
def plot_country_data(matrix, countries, country):
    if country not in countries:
        return None
    y = matrix[countries == country][0]
    x = [i for i in range(matrix.shape[1])]
    plt.plot(x,y, color = 'r')
    plt.xlabel('Days', fontsize=16)
    plt.title(country, fontsize=16)
    plt.show()


#########################################
# Question B3.2 - do not delete this comment
#########################################
def plot_top_countries(matrix, countries):
    sum_all_countries = np.sum(matrix, axis=1)
    sorted_sum = sorted(sum_all_countries, reverse=True)
    bool_sum = sum_all_countries > sorted_sum[10]
    top_ten_countries = countries[bool_sum]
    x = [i for i in range(matrix.shape[1])]
    for country in top_ten_countries:
        y = matrix[countries == country][0]
        plt.plot(x, y, label=country)
    plt.legend()
    plt.title('Top 10 countries')
    plt.xlabel('Days')
    plt.show()

#########################################
# Question B3.3 - do not delete this comment
#########################################
def draw_covid_heatmap(matrix, countries):
    matrix[matrix < 1] = 1
    matrix = np.log2(matrix)
    ids = np.argsort(matrix[:, :100].sum(axis=1))[::-1][:20]
    top_20_countries = countries[ids[::-1]]
    data = matrix[ids[::-1]]
    plt.imshow(data, cmap='afmhot', interpolation='none', aspect='auto')
    plt.yticks(range(len(top_20_countries)), top_20_countries)
    plt.colorbar()
    plt.show()


#Testing your code -------------------------------
countries, dates, matrix = load_covid_world_matrix('owid-covid-data_2-1-2021.csv', 'new_cases')
np.savetxt("matrix_new_cases.csv", matrix, delimiter=",", fmt='%f')
np.savetxt("dates_new_cases.csv", dates, delimiter=",", fmt='%s')
np.savetxt("countries_new_cases.csv", countries, delimiter=",", fmt='%s')

print(countries.shape)
print(dates.shape)
print(matrix.shape)
print(matrix.sum())

analyze_covid_data(countries, dates, matrix)

plot_country_data(matrix, countries, 'Israel')
plot_top_countries(matrix, countries)
draw_covid_heatmap(matrix, countries)

