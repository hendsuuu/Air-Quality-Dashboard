import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df  = pd.read_csv('all_data.csv')
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    st.title("Analisis Dataset Air Quality Kota Gucheng dan Guanyuan")

    menu  = ["Home","Dataset","EDA","Question"]
    st.sidebar.title("Menu")
    pilihan = st.sidebar.selectbox("Menu",menu)


    if pilihan == "Home":
        st.subheader("Home")
    elif pilihan == "Dataset":
        st.subheader("Dataset")
        st.dataframe(df)
    elif pilihan == "EDA":
        st.subheader("Exploratory Data Analysis")
        # korelasi=df.corr()
        # st.dataframe(korelasi)
        st.pyplot(corr())
        st.pyplot(avg_yearly_summary())
        
        
        st.write("Ringkasan analisis tahunan di Gucheng dan Guanyuan,kadar polutan yang ditampilkan yaitu PM2.5, PM10, SO2, NO2 , dan CO untuk CO saya pisahkan sendiri karena nilainya yang terlalu besar dibanding field yang lain bertujuan agar dapat terlihat jelas untuk visualisasi datanya")
        yearly_summary(['PM2.5', 'PM10', 'SO2', 'NO2'],'Gucheng')
        yearly_summary(['CO'],'Gucheng')
        yearly_summary(['PM2.5', 'PM10', 'SO2', 'NO2'],'Guanyuan')
        yearly_summary(['CO'],'Guanyuan')
    else :
        st.subheader("Question")
        st.write("Pertanyaan 1: Bagaimana kondisi harian udara di gucheng dan guanyuan,pada jam berapa kadar polutan cenderung tinggi?")
        stations = df['station'].unique()
        question1(['PM2.5', 'PM10', 'SO2', 'NO2'], stations[:2], '2016-01-01')
        st.write("Pertanyaan 2: Bagaimana Ringkasan kadar polutan Tahunan di Gucheng dan Guanyuan pada bulan januari 2016?")
        st.write("Conclusion :")
        st.write("Pada grafik diaas merupakan data polutan pada tanggal januari 2016 di gucheng dan guanyuan.X merupakan Jam dalam sehari sedangkan Y merupakan tingkat konsntrasi polutan.dari grafik kita dapat menyimpulkan kadar polutan cendeerung tinggi pada jam sore-malam.polutan mulai mengalami kenaikan pada sekitar jam 16 hingga mencapai titik tertinggi pada jam 22 di kota gucheng.hal tersebut menunjukkan")
        
        
        # start_date = st.date_input("Pilih tanggal Mulai")
        # end_date = st.date_input("Pilih tanggal Akhir")
        question2('2016-01-01', '2016-01-31',['PM2.5','PM10','SO2','NO2'])
        st.write("Conclusion :")
        st.write("Visualisasi data kadar polutan yang ada di Gucheng dan guanyuan mulai 1 januari 2016 sampai 31 januari 2016 Grafik diatas berisi informasi tentang kadar polutan yang ada,garis tengah menunjukkan rata2 kadar polutan dalam sehari sedangkan offside dari garis tersebut menunjukkan data tertinggi dan data terendah kadar polutan dalam seharinya.kadar polutan pada tahun 2016 cenderung tinggi pada tanggal 1-2 januari.pada grafik diatas cenderung naik turun unuk kadar polutan.naik saat weekend dan cenederung turun disaat weekday mungkin dikarenakan jalur lalu lintas yang tinggi saat weekend")

def corr():
    st.write("Visualisasi korelasi antar field,Merah melambagkan korelasi positif antar field contoh PM2.5 memiliki tingka korelasi 0.87 dengan PM10 artinya nilai antara PM2.5 linear dengan PM10 jika PM2.5 memiliki nilai yang tinggi maka otomatis pm 10 juga akan meiliki nilai yang tinggi dan sebaliknya jika memiliki korelasi negatif suatu nilai akan berkebalikan dengan nilai lainnya conohnya antara PRES dan TEMP , PRES merupakan tekanan udara sedangkan TEMP adalah temperatur, jika TEMP tinggi maka PRES akan rendah nilainya dan sebaliknya.")
    kolom_korelasi = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']


    korelasi = df[kolom_korelasi].corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(korelasi, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Heatmap Korelasi')
    plt.show()

def yearly_summary(fields,station):
    yearly_monthly_mean = df.groupby(['year', 'month','station']).mean(numeric_only=True).reset_index()

    # Mendapatkan daftar tahun unik dari dataset
    years = df['year'].unique()

    # Mendapatkan daftar bulan unik dan diurutkan dari dataset
    monthly = df['month'].unique()
    monthly.sort()


    # Membuat plot untuk setiap tahun
    for i,year in enumerate(years):
        yearly_data = yearly_monthly_mean[(yearly_monthly_mean['year'] == year )& (yearly_monthly_mean['station'] == station)]

        # Membuat plot untuk setiap polutan dalam satu gambar
        fig, axes = plt.subplots(1, 1, figsize=(15, 6))

        for polutan in fields:
            plt.plot(yearly_data['month'], yearly_data[polutan], label=polutan,marker='o')

        plt.xlabel('Bulan')
        plt.ylabel('Rata-rata Kualitas Udara')
        # plt.title(f'Rata-rata Kadar Polutan per Bulan di {station} - Tahun {year}')
        st.write(f'Rata-rata Kadar Polutan per Bulan di {station} - Tahun {year}')
        plt.legend()
        plt.grid(True)
        plt.xticks(monthly)
        plt.tight_layout()
        st.pyplot(fig)
        
        
def avg_yearly_summary():
    st.write("Rata rata kadar polutan tiap tahun")
    # df['year'] = df['date'].dt.year

    # Agregasi data berdasarkan tahun
    annual_mean = df.groupby('year').mean(numeric_only=True)

    # Visualisasi tren kualitas udara dari tahun ke tahun
    plt.figure(figsize=(10, 6))
    plt.plot(annual_mean.index, annual_mean['PM2.5'], marker='o', label='PM2.5')
    plt.plot(annual_mean.index, annual_mean['PM10'], marker='o', label='PM10')
    plt.plot(annual_mean.index, annual_mean['SO2'], marker='o', label='SO2')
    plt.plot(annual_mean.index, annual_mean['NO2'], marker='o', label='NO2')
    # plt.plot(annual_mean.index, annual_mean['CO'], marker='o', label='CO')
    plt.title('Tren Kualitas Udara dari Tahun ke Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata Kualitas Udara')
    plt.legend()
    plt.grid(True)

def get_data(station, date):
    data = df.loc[(df['date'] == date) & (df['station'] == station)]
    return data


def question1(polutan, stations,date):
    # data = df.loc[(df['date'] == date) & (df['station'] == stations)]
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    fig.suptitle(f'Pembandingan Kualitas Udara Polutan per Jam pada {date}', y=0.98)

    for i, station in enumerate(stations):
        data_station = get_data(station, date)
        for pol in polutan:
            axes[i].plot(data_station['hour'], data_station[pol], marker='o', linestyle='-', label=f'{pol} - {station}')
            axes[i].set_title(f'Kualitas Udara di {station}')
            axes[i].set_xlabel('Jam dalam Sehari')
            axes[i].set_ylabel('Konsentrasi Polutan')
            axes[i].grid(True)
            axes[i].legend()

    plt.tight_layout()
    st.pyplot(fig)


def question2(start_date, end_date,content_value):
    # df['date'] = pd.to_datetime(df['date']).floor('D')

    # Filter data berdasarkan tanggal mulai dan akhir
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    stations = filtered_data['station'].unique()

    num_rows = 1
    num_cols = 2

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 8))
    axes = axes.flatten()  # Mengubah matriks 2D menjadi array 1D

    contents = content_value

    for i, station in enumerate(stations):
        station_data = filtered_data[filtered_data['station'] == station]

        for content in contents:
            sns.lineplot(data=station_data, x='date', y=content, ax=axes[i], label=content,)


        axes[i].set_title(station)

        if i >= num_cols * (num_rows - 1):
            axes[i].set_xlabel('Date')

        axes[i].tick_params(axis='x', rotation=45)
        axes[i].set_ylabel('PPM')

        if i == len(stations) - 1:
            axes[i].legend()

    plt.tight_layout()
    st.pyplot(fig)
    
if __name__ == '__main__':
    main()
        
        
