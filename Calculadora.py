import tkinter as tk
from tkinter import messagebox
import math

# Funciones de cálculo
def calcular_pago_mensual(monto_prestamo, tasa_interes_mensual, plazo_en_meses):
    if tasa_interes_mensual == 0:
        return monto_prestamo / plazo_en_meses
    return (monto_prestamo * tasa_interes_mensual) / (1 - (1 + tasa_interes_mensual) ** -plazo_en_meses)

def calcular_total_intereses_pagados(monto_prestamo, pago_mensual, plazo_en_meses):
    total_pagado = pago_mensual * plazo_en_meses
    total_intereses = total_pagado - monto_prestamo
    return total_intereses

def calcular_meses_para_pagar(monto_prestamo, pago_mensual, tasa_interes_mensual):
    if tasa_interes_mensual == 0:
        return monto_prestamo / pago_mensual
    meses = -1 * (math.log(1 - (monto_prestamo * tasa_interes_mensual) / pago_mensual) / math.log(1 + tasa_interes_mensual))
    return int(math.ceil(meses))

def calcular_amortizacion(monto_prestamo, tasa_interes_mensual, plazo_en_meses):
    pago_mensual = calcular_pago_mensual(monto_prestamo, tasa_interes_mensual, plazo_en_meses)
    amortizacion_detallada = []

    saldo_restante = monto_prestamo
    for mes in range(1, plazo_en_meses + 1):
        interes_mes = saldo_restante * tasa_interes_mensual
        amortizacion_principal = pago_mensual - interes_mes
        saldo_restante -= amortizacion_principal
        detalle_mes = {
            "Mes": mes,
            "Pago Mensual": pago_mensual,
            "Interés Pagado": interes_mes,
            "Amortización Principal": amortizacion_principal,
            "Saldo Restante": saldo_restante
        }
        amortizacion_detallada.append(detalle_mes)

    return amortizacion_detallada

def mostrar_detalle_amortizacion(detalle_amortizacion):
    resultado = "{:<5} {:<15} {:<15} {:<20} {:<20}\n".format("Mes", "Pago Mensual", "Interés Pagado", "Amortización Principal", "Saldo Restante")
    resultado += "-" * 75 + "\n"
    for detalle in detalle_amortizacion:
        resultado += "{:<5} ${:<14.2f} ${:<14.2f} ${:<19.2f} ${:<19.2f}\n".format(
            detalle["Mes"], detalle["Pago Mensual"], detalle["Interés Pagado"],
            detalle["Amortización Principal"], detalle["Saldo Restante"]
        )
    return resultado

# Función para limpiar los valores de entrada
def limpiar_valor(valor):
    return valor.replace(',', '').replace(' ', '')

# Función de validación y cálculo
def on_calculate(option, entry_values, tasa_periodo_var):
    try:
        monto_prestamo = float(limpiar_valor(entry_values[0].get()))
        tasa_interes_anual = float(limpiar_valor(entry_values[1].get()))
        plazo_en_meses = entry_values[2].get()
        pago_mensual_conocido = entry_values[3].get()
        tasa_periodo = int(tasa_periodo_var.get())

        if tasa_interes_anual < 0:
            raise ValueError("La tasa de interés no puede ser negativa.")

        # Ajustar la tasa de interés a una base mensual
        if tasa_periodo == 1:  # Mensual
            tasa_interes_mensual = tasa_interes_anual / 12 / 100
        else:  # Cualquier otro periodo
            tasa_interes_mensual = (1 + tasa_interes_anual / 100) ** (tasa_periodo / 12) - 1

        if option in (1, 2, 4):
            plazo_en_meses = int(plazo_en_meses)

        if option == 1:
            pago_mensual = calcular_pago_mensual(monto_prestamo, tasa_interes_mensual, plazo_en_meses)
            messagebox.showinfo("Resultado", "El pago mensual es: ${:.2f}".format(pago_mensual))

        elif option == 2:
            pago_mensual = calcular_pago_mensual(monto_prestamo, tasa_interes_mensual, plazo_en_meses)
            total_intereses = calcular_total_intereses_pagados(monto_prestamo, pago_mensual, plazo_en_meses)
            messagebox.showinfo("Resultado", "El total de intereses pagados será: ${:.2f}".format(total_intereses))

        elif option == 3:
            if not pago_mensual_conocido:
                raise ValueError("Debe ingresar un valor para el pago mensual.")
            pago_mensual = float(limpiar_valor(pago_mensual_conocido))
            if pago_mensual <= 0:
                raise ValueError("El pago mensual debe ser mayor que cero.")
            meses_para_pagar = calcular_meses_para_pagar(monto_prestamo, pago_mensual, tasa_interes_mensual)
            messagebox.showinfo("Resultado", "Se necesitarán aproximadamente {} meses para pagar el préstamo.".format(meses_para_pagar))

        elif option == 4:
            detalle_amortizacion = calcular_amortizacion(monto_prestamo, tasa_interes_mensual, plazo_en_meses)
            resultado = mostrar_detalle_amortizacion(detalle_amortizacion)
            messagebox.showinfo("Detalle de Amortización", resultado)

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except ZeroDivisionError:
        messagebox.showerror("Error", "No se puede dividir por cero. Verifique las entradas.")

# Función para gestionar la habilitación de campos
def update_fields(option, entry_fields):
    if option == 3:
        entry_fields[2].config(state='disabled')  # Plazo en meses
        entry_fields[3].config(state='normal')    # Pago mensual
    else:
        entry_fields[2].config(state='normal')    # Plazo en meses
        entry_fields[3].config(state='disabled')  # Pago mensual

# Función para mostrar información sobre la aplicación
def mostrar_informacion():
    info_texto = (
        "Esta es una calculadora de amortización de préstamos.\n\n"
        "Opciones disponibles:\n"
        "1. Calcular el pago mensual del préstamo.\n"
        "2. Calcular el total de intereses pagados.\n"
        "3. Calcular los meses necesarios para pagar el préstamo dado un pago mensual conocido.\n"
        "4. Mostrar el detalle de amortización mensual.\n\n"
        "Ingrese el monto del préstamo, la tasa de interés anual y el plazo en meses para realizar los cálculos. "
        "Seleccione la opción deseada y haga clic en 'Calcular'."
    )
    messagebox.showinfo("Información de la Aplicación", info_texto)

# Función para cambiar entre modo claro y oscuro
def toggle_theme(root, labels, entries, radio_buttons, is_dark_mode):
    if is_dark_mode.get():
        bg_color = "#2E2E2E"
        fg_color = "#FFFFFF"
        entry_bg = "#4D4D4D"
        entry_fg = "#FFFFFF"
    else:
        bg_color = "#FFFFFF"
        fg_color = "#000000"
        entry_bg = "#FFFFFF"
        entry_fg = "#000000"

    root.config(bg=bg_color)
    for label in labels:
        label.config(bg=bg_color, fg=fg_color)
    for entry in entries:
        entry.config(bg=entry_bg, fg=entry_fg)
    for radio_button in radio_buttons:
        radio_button.config(bg=bg_color, fg=fg_color)
    info_button.config(bg=bg_color, fg=fg_color)
    theme_button.config(bg=bg_color, fg=fg_color)
    calculate_button.config(bg=bg_color, fg=fg_color)

# Crear la interfaz gráfica
def create_gui():
    global info_button, theme_button, calculate_button
    root = tk.Tk()
    root.title("Calculadora de Amortización")

    # Crear un botón de información en la parte superior derecha
    info_button = tk.Button(root, text="Info", command=mostrar_informacion)
    info_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

    labels = [
        "Monto del préstamo:",
        "Tasa de interés anual (%):",
        "Plazo en meses:",
        "Pago mensual (si ya se conoce):"
    ]
    entry_values = []
    label_objects = []

    for i, label_text in enumerate(labels):
        label = tk.Label(root, text=label_text)
        label.grid(row=i+1, column=0, padx=10, pady=10)
        entry = tk.Entry(root)
        entry.grid(row=i+1, column=1, padx=10, pady=10)
        entry_values.append(entry)
        label_objects.append(label)

    option_var = tk.IntVar()
    option_var.set(1)
    options = [
        ("Pago mensual", 1),
        ("Total de intereses pagados", 2),
        ("Meses para pagar", 3),
        ("Detalle de amortización mensual", 4)
    ]
    radio_buttons = []

    for text, value in options:
        radio_button = tk.Radiobutton(
            root, text=text, variable=option_var, value=value,
            command=lambda: update_fields(option_var.get(), entry_values)
        )
        radio_button.grid(columnspan=2, padx=10, sticky=tk.W)
        radio_buttons.append(radio_button)

    tasa_periodo_var = tk.IntVar()
    tasa_periodo_var.set(12)  # Default to annual

    periodo_options = [("Mensual", 1), ("Trimestral", 3), ("Semestral", 6), ("Anual", 12)]
    for text, value in periodo_options:
        periodo_radio_button = tk.Radiobutton(root, text=text, variable=tasa_periodo_var, value=value)
        periodo_radio_button.grid(columnspan=2, padx=10, sticky=tk.W)
        radio_buttons.append(periodo_radio_button)

    calculate_button = tk.Button(root, text="Calcular", command=lambda: on_calculate(option_var.get(), entry_values, tasa_periodo_var))
    calculate_button.grid(row=len(labels)+8, columnspan=2, padx=10, pady=10)

    # Botón para cambiar entre modo claro y oscuro
    is_dark_mode = tk.BooleanVar()
    theme_button = tk.Checkbutton(root, text="Modo Oscuro", variable=is_dark_mode, command=lambda: toggle_theme(root, label_objects, entry_values, radio_buttons, is_dark_mode))
    theme_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    update_fields(option_var.get(), entry_values)  # Initial call to set field states

    root.mainloop()

if __name__ == "__main__":
    create_gui()
