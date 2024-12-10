import pandas as pd
import plotly.graph_objects as go
from django.shortcuts import render, redirect
from .models import DataPoint
from .forms import DataPointForm
from django.contrib import messages

def landing(request):
    return render(request, 'data_visualizer/base.html')

def index(request):
    if request.method == 'POST':
        form = DataPointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DataPointForm()

    data_points = DataPoint.objects.all()
    df = pd.DataFrame(list(data_points.values()))

    chart_type = request.GET.get('chart_type', 'scatter')

    if not df.empty:
        if chart_type == 'scatter':
            fig = go.Figure(data=go.Scatter(x=df['x_value'], y=df['y_value'], mode='markers'))
        elif chart_type == 'bar':
            fig = go.Figure(data=go.Bar(x=df['x_value'], y=df['y_value']))
        elif chart_type == 'pie':
            fig = go.Figure(data=go.Pie(labels=df['x_value'], values=df['y_value']))
        elif chart_type == 'line':
            fig = go.Figure(data=go.Scatter(x=df['x_value'], y=df['y_value'], mode='lines'))
        elif chart_type == 'area':
            fig = go.Figure(data=go.Scatter(x=df['x_value'], y=df['y_value'], fill='tozeroy'))
        elif chart_type == 'box':
            fig = go.Figure(data=go.Box(y=df['y_value'], name='Distribución'))
        elif chart_type == 'histogram':
            fig = go.Figure(data=go.Histogram(x=df['y_value']))
        else:
            fig = go.Figure(data=go.Scatter(x=df['x_value'], y=df['y_value'], mode='markers'))

        fig.update_layout(title='Visualización de Datos', xaxis_title='Valor X', yaxis_title='Valor Y')
        plot_div = fig.to_html(full_html=False)

        total_sum = round(df['y_value'].sum(), 2)
        average = round(df['y_value'].mean(), 2)

        context = {
            'form': form,
            'plot_div': plot_div,
            'total_sum': total_sum,
            'average': average,
            'chart_type': chart_type,
        }
    else:
        context = {'form': form}

    return render(request, 'data_visualizer/index.html', context)

def delete_all_data(request):
    if request.method == 'POST':
        DataPoint.objects.all().delete()
        messages.success(request, 'Todos los datos han sido eliminados.')
    return redirect('index')

def import_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'Por favor, sube un archivo Excel válido.')
            return redirect('index')

        df = pd.read_excel(excel_file)
        for _, row in df.iterrows():
            DataPoint.objects.create(
                x_value=str(row[0]),
                y_value=float(row[1]),
                source='excel'
            )
        messages.success(request, 'Datos importados exitosamente desde Excel.')
    return redirect('index')