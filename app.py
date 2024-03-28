import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def main():
    with st.sidebar: 
        st.title("Instrucciones")
        st.write("¡Bienvenido a la aplicación de Diagrama de Proceso!")
        st.markdown("Por favor sigue las instrucciones paso a paso para utilizar la herramienta correctamente.")
        
        # Pasos para el Diagrama de Proceso
        st.markdown("### Pasos:")
        st.markdown("- **Paso 1:** Ingresa el número de actividades.")
        st.markdown("- **Paso 2:** Para cada actividad, ingresa el nombre, tiempo, distancia recorrida y tipo.")
        st.markdown("- **Paso 3:** Observa los gráficos que muestran el tiempo y la distancia por actividad.")
        st.markdown("- **Paso 4:** ¡Listo! Puedes ver los datos ingresados en la tabla debajo de los gráficos y descargarlos como un archivo Excel.")
        
        # Ejemplos de tipos de actividad con símbolos
        st.markdown("### Ejemplos de Tipos de Actividad:")
        st.markdown("- **Operación:** 🟩")
        st.markdown("- **Transporte:** ➡️")
        st.markdown("- **Inspección:** 🟡")
        st.markdown("- **Almacenamiento:** 🔺")
        st.markdown("- **Espera:** 🔴")
        
        # Información adicional
        st.markdown("### Información Adicional:")
        st.markdown("👉 **Para más información: [LinkedIn](https://www.linkedin.com/in/josemaguilar/)**")

    st.image("diagrama.jpg", width=720) 

    st.sidebar.header("Diagrama de Proceso")

    num_activities = st.sidebar.number_input('Número de Actividades', min_value=1, step=1, value=1, format='%d')

    if num_activities < 1:
        st.sidebar.warning("Debe ingresar al menos una actividad.")
        return

    activities_data = []

    for i in range(num_activities):
        st.sidebar.markdown(f"**Actividad {i+1}**")
        activity_name = st.sidebar.text_input(f'Nombre de la Actividad - Actividad {i+1}')
        activity_time = st.sidebar.number_input(f'Tiempo de la Actividad (min) - Actividad {i+1}', min_value=0.0, step=0.1, value=0.0)
        activity_distance = st.sidebar.number_input(f'Distancia Recorrida (km) - Actividad {i+1}', min_value=0.0, step=0.1, value=0.0)
        activity_type = st.sidebar.selectbox(f'Tipo de Actividad - Actividad {i+1}', ['Operación', 'Transporte', 'Inspección', 'Espera', 'Almacen'])
        
        activities_data.append((activity_name, activity_time, activity_distance, activity_type))

    plot_process_diagram(activities_data)

    # Convertir los datos en un DataFrame de Pandas
    df = pd.DataFrame(activities_data, columns=['Nombre de la Actividad', 'Tiempo (min)', 'Distancia (km)', 'Tipo de Actividad'])
    
    # Reemplazar los nombres de los tipos de actividad con los símbolos correspondientes
    df['Tipo de Actividad'] = df['Tipo de Actividad'].replace({
        'Operación': '🟩',
        'Transporte': '➡️',
        'Inspección': '🟡',
        'Almacen': '🔺',
        'Espera': '🔴'
    })
    
    st.write(df)

    # Botón para descargar el DataFrame como archivo Excel
    if st.button('Descargar datos como Excel'):
        st.download_button(label='Descargar',
                           data=df.to_csv().encode('utf-8'),
                           file_name='actividades_diagrama.xlsx',
                           mime='application/octet-stream')

def plot_process_diagram(activities_data):
    activity_names = [data[0] for data in activities_data]
    activity_times = [data[1] for data in activities_data]
    activity_distances = [data[2] for data in activities_data]
    activity_types = [data[3] for data in activities_data]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    colors = get_colors(activity_types)

    ax1.bar(activity_names, activity_times, color=[colors[activity_type] for activity_type in activity_types])
    ax1.set_ylabel('Tiempo (minutos)')
    ax1.set_xlabel('Actividades')
    ax1.set_title('Diagrama de Proceso - Tiempo por Actividad')
    ax1.grid(True)

    ax2.bar(activity_names, activity_distances, color=[colors[activity_type] for activity_type in activity_types])
    ax2.set_ylabel('Distancia (km)')
    ax2.set_xlabel('Actividades')
    ax2.set_title('Diagrama de Proceso - Distancia por Actividad')
    ax2.grid(True)

    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in set(activity_types)]
    ax1.legend(handles, set(activity_types))

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

if __name__ == "__main__":
    main()
