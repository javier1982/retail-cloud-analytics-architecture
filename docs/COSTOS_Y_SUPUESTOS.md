# Costos, consumo y supuestos de la arquitectura

## 1. Propósito

Este documento describe los supuestos utilizados para analizar el consumo técnico y el costo operativo asociado a la arquitectura presentada en el artículo:

**“Arquitectura analítica cloud de bajo costo de entrada para PYMEs del sector retail”.**

El análisis no pretende calcular un costo total de propiedad empresarial.

Su alcance se limita a los componentes técnicos directamente observables durante el experimento, principalmente:

- almacenamiento;
- procesamiento de consultas;
- volumen de datos leído;
- estimación previa mediante Dry Run;
- comportamiento de consultas seleccionadas.

---

## 2. Definición de “bajo costo de entrada”

En este proyecto, el término **bajo costo de entrada** describe una arquitectura que puede ponerse en funcionamiento sin desplegar infraestructura dedicada ni adquirir inicialmente una plataforma analítica empresarial completa.

El concepto se fundamenta en:

- uso de servicios administrados;
- pago según consumo;
- ausencia de servidores dedicados;
- utilización de Google Colab;
- uso de BigQuery bajo demanda;
- control previo de consultas mediante Dry Run;
- selección de columnas;
- almacenamiento reducido en el escenario experimental;
- generación de un dashboard portable;
- ausencia de una infraestructura permanente para servir el dashboard.

El término no significa que toda implementación futura tenga costo cero.

---

## 3. Alcance económico

La evaluación realizada corresponde a una:

**estimación técnica de consumo y costo operativo asociado a consulta y almacenamiento.**

No constituye una evaluación económica integral.

No se incluyen en el cálculo:

- horas de desarrollo;
- salarios;
- capacitación;
- soporte;
- mantenimiento;
- migración;
- gobierno de datos;
- administración de usuarios;
- seguridad empresarial;
- monitoreo;
- continuidad del negocio;
- integración con sistemas corporativos;
- operación del área de tecnología.

Por tanto, los resultados no representan un TCO universal.

---

## 4. Modelo de facturación considerado

La reproducción utiliza como referencia el modelo:

```text
Google BigQuery
Modalidad:
On-demand
```

En este modelo, el procesamiento de consultas se factura principalmente de acuerdo con el volumen de datos procesados.

La documentación oficial vigente debe consultarse antes de cualquier nueva evaluación económica, ya que los precios pueden variar por región, modalidad o cambios del proveedor.

---

## 5. Referencia de precios

Fecha de referencia documental:

```text
7 de noviembre de 2026
```

Moneda:

```text
USD
```

Referencia general de BigQuery bajo demanda:

```text
Procesamiento de consultas:
desde USD 6,25 / TiB procesado
```

La documentación oficial de Google Cloud indica además que:

```text
Primer 1 TiB de consultas
bajo demanda por mes:
sin cargo
```

Para almacenamiento lógico, Google Cloud publica precios desde:

```text
USD 0,01 / GiB por mes
```

con un nivel gratuito inicial de almacenamiento sujeto a las condiciones vigentes del servicio.

Los precios reales deben verificarse para la región y configuración utilizadas en cada reproducción.

---

## 6. Mínimos de facturación

BigQuery aplica mínimos de procesamiento facturable en el modelo bajo demanda.

Como referencia técnica:

```text
Mínimo por consulta:
10 MiB
```

y, cuando una consulta referencia tablas:

```text
Mínimo por tabla referenciada:
10 MiB
```

Esto tiene una consecuencia importante para el experimento.

Aunque Dry Run puede mostrar que una consulta selecciona un volumen bruto inferior a 10 MiB, el ahorro técnico de bytes procesados no necesariamente se transforma en una reducción monetaria proporcional cuando la consulta permanece por debajo del mínimo facturable.

---

## 7. Implicación para este estudio

El conjunto utilizado ocupa aproximadamente:

```text
3,01 MiB
```

Por ello, las consultas evaluadas operan sobre un volumen muy pequeño.

La reducción de bytes observada demuestra:

- selección más eficiente de datos;
- menor lectura lógica;
- mejor diseño de consultas;
- potencial de ahorro cuando el volumen aumenta.

Sin embargo, en el tamaño actual del experimento no debe afirmarse que cada reducción porcentual produzca un ahorro monetario equivalente.

---

## 8. Dry Run

BigQuery Dry Run permite estimar el volumen que procesaría una consulta antes de ejecutarla.

Ejemplo:

```python
from google.cloud import bigquery

job_config = bigquery.QueryJobConfig(
    dry_run=True,
    use_query_cache=False
)

query_job = client.query(
    query,
    job_config=job_config
)

bytes_processed = (
    query_job.total_bytes_processed
)

print(bytes_processed)
```

Dry Run permite analizar el consumo previsto sin ejecutar la consulta.

---

## 9. Utilidad de Dry Run

El mecanismo permite:

- detectar consultas excesivas;
- comparar alternativas SQL;
- estimar procesamiento;
- evitar ejecuciones innecesarias;
- establecer barreras de consumo;
- tomar decisiones antes de ejecutar.

Por esta razón forma parte del mecanismo de control de consumo de la arquitectura.

---

## 10. Consulta de referencia

La consulta utilizada como línea base es:

```sql
SELECT *
FROM
    `PROJECT_ID.retail_analytics.superstore_sales`;
```

En el escenario documentado se estimaron aproximadamente:

```text
3,0111 MiB
```

de datos procesados para la consulta completa.

---

## 11. Consulta de ventas y beneficio

```sql
SELECT
    sales,
    profit
FROM
    `PROJECT_ID.retail_analytics.superstore_sales`;
```

Dry Run documentado:

```text
0,1525 MiB
```

Reducción técnica respecto de `SELECT *`:

```text
94,93 %
```

---

## 12. Consulta agrupada por categoría

```sql
SELECT
    category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM
    `PROJECT_ID.retail_analytics.superstore_sales`
GROUP BY
    category;
```

Dry Run documentado:

```text
0,2936 MiB
```

Reducción aproximada:

```text
90,25 %
```

---

## 13. Consulta de productos principales

```sql
SELECT
    product_name,
    SUM(sales) AS total_sales
FROM
    `PROJECT_ID.retail_analytics.superstore_sales`
GROUP BY
    product_name
ORDER BY
    total_sales DESC
LIMIT 10;
```

Dry Run documentado:

```text
0,4487 MiB
```

Reducción aproximada:

```text
85,10 %
```

---

## 14. Fórmula de reducción

La reducción porcentual puede calcularse mediante:

```text
Reducción (%) =
((Bytes_base - Bytes_consulta)
/
Bytes_base)
× 100
```

Ejemplo:

```python
reduction = (
    (base_bytes - query_bytes)
    / base_bytes
) * 100
```

---

## 15. Interpretación correcta de las reducciones

Los porcentajes:

```text
94,93 %
90,25 %
85,10 %
```

representan reducción técnica del volumen estimado de datos procesados respecto de la consulta de referencia.

No representan automáticamente:

- ahorro monetario equivalente;
- reducción universal;
- ahorro garantizado en otros datasets;
- ahorro garantizado en todas las regiones;
- disminución del TCO.

---

## 16. Fórmula conceptual de costo de consulta

Para un escenario en el que el volumen facturable supera los niveles gratuitos y mínimos aplicables, puede utilizarse conceptualmente:

```text
Costo estimado =
TiB facturables
×
precio por TiB
```

Conversión:

```text
TiB =
bytes facturables
/
(1024^4)
```

Ejemplo en Python:

```python
TIB = 1024 ** 4

processed_tib = (
    billable_bytes / TIB
)

estimated_cost = (
    processed_tib
    * price_per_tib
)
```

---

## 17. Consideración del nivel gratuito

Antes de interpretar un costo estimado debe considerarse:

```text
Nivel gratuito mensual disponible
```

Cuando el consumo total permanece dentro del nivel gratuito vigente, el costo directo de procesamiento puede ser:

```text
USD 0
```

aunque exista consumo técnico medido en bytes.

Por ello deben diferenciarse:

```text
Consumo técnico
≠
Costo monetario facturado
```

---

## 18. Mínimo facturable

Para consultas pequeñas debe utilizarse como referencia el mínimo aplicable del proveedor.

Conceptualmente:

```text
Bytes facturables =
máximo(
    bytes procesados,
    mínimo facturable
)
```

Este comportamiento debe considerarse antes de convertir directamente los resultados de Dry Run en dólares.

---

## 19. Barrera de consumo mediante maximumBytesBilled

BigQuery permite establecer un límite máximo de bytes facturables.

Ejemplo:

```python
job_config = bigquery.QueryJobConfig(
    maximum_bytes_billed=100_000_000
)
```

Si la estimación supera el límite definido, la consulta puede rechazarse antes de ejecutarse.

Este mecanismo permite establecer controles adicionales sobre consultas bajo demanda.

---

## 20. Proyección de almacenamiento

A partir del tamaño observado en el conjunto experimental se calculó una proyección teórica.

Valores aproximados:

| Registros | Almacenamiento proyectado |
|---:|---:|
| 10.000 | 3,01 MiB |
| 100.000 | 30,13 MiB |
| 1.000.000 | 301,29 MiB |
| 10.000.000 | 2,9423 GiB |

Esta tabla representa únicamente una:

**proyección teórica de almacenamiento.**

---

## 21. Fórmula de proyección

Si el tamaño medio aproximado por registro permanece constante:

```text
Tamaño proyectado =
número de registros
×
bytes promedio por registro
```

En el experimento se obtuvo aproximadamente:

```text
315,93 bytes por registro
```

Este valor es específico de:

- este dataset;
- su esquema;
- sus tipos de datos;
- la representación utilizada.

---

## 22. Lo que la proyección no demuestra

La proyección a diez millones de registros no demuestra:

- rendimiento;
- latencia;
- concurrencia;
- escalabilidad completa;
- comportamiento productivo;
- tiempos de actualización;
- capacidad de usuarios simultáneos.

Estos aspectos requieren experimentación específica.

---

## 23. Almacenamiento

La tabla utilizada durante el experimento presenta un tamaño aproximado de:

```text
3,0111 MiB
```

Este volumen se encuentra muy por debajo de los niveles de almacenamiento habituales de una plataforma analítica empresarial.

Sin embargo, este resultado corresponde solamente al banco de pruebas utilizado.

---

## 24. Dashboard y costos operativos

El dashboard generado se almacena como un archivo HTML portable.

No requiere una conexión permanente con BigQuery.

El flujo es:

```text
BigQuery
    ↓
DataFrame
    ↓
JSON
    ↓
HTML
```

Esto permite consultar el dashboard generado sin ejecutar una nueva consulta BigQuery durante cada interacción local del usuario.

---

## 25. Limitación del dashboard

El beneficio anterior implica una contrapartida:

el dashboard no refleja cambios en tiempo real.

Para actualizar la información debe volver a ejecutarse el proceso:

```text
consulta
→
recuperación
→
serialización
→
generación del dashboard
```

---

## 26. Costos no modelados

El estudio no cuantifica:

```text
desarrollo
mantenimiento
soporte
personal
capacitación
seguridad
gobierno de datos
integraciones
migración
gestión organizacional
```

Por ello no debe utilizarse el experimento como una estimación completa del costo empresarial de adopción.

---

## 27. Interpretación del concepto de bajo costo

La conclusión válida es:

**la arquitectura presenta un bajo costo de entrada dentro del escenario técnico evaluado y bajo los supuestos documentados.**

No debe afirmarse:

```text
“Esta arquitectura siempre será más barata
que cualquier alternativa”.
```

Tampoco:

```text
“El costo total de implementar
la solución es prácticamente cero”.
```

---

## 28. Comparación con otras plataformas

Las referencias a herramientas como:

- Power BI;
- Looker Studio;
- PostgreSQL;
- otras plataformas analíticas;

tienen carácter conceptual.

El estudio no ejecutó un benchmark económico completo entre proveedores.

Por tanto, no se afirma superioridad económica experimental frente a estas plataformas.

---

## 29. Factores que pueden modificar el costo

El costo real puede variar según:

- región;
- modalidad de facturación;
- cantidad de datos;
- frecuencia de consultas;
- complejidad SQL;
- almacenamiento;
- transferencias;
- servicios adicionales;
- usuarios;
- actualizaciones de precios.

---

## 30. Recomendación para futuras reproducciones

Antes de ejecutar una evaluación económica se recomienda:

1. consultar la página oficial de precios;
2. registrar la fecha de consulta;
3. registrar la región utilizada;
4. identificar la modalidad de facturación;
5. documentar el nivel gratuito vigente;
6. ejecutar Dry Run;
7. registrar bytes procesados;
8. considerar mínimos facturables;
9. separar consumo de costo monetario;
10. evitar extrapolar directamente el costo experimental hacia un TCO empresarial.

---

## 31. Fuentes oficiales

La información vigente sobre precios y control de costos debe consultarse en la documentación oficial de Google Cloud.

BigQuery Pricing:

```text
https://cloud.google.com/bigquery/pricing
```

Estimate and control costs:

```text
https://cloud.google.com/bigquery/docs/best-practices-costs
```

Las condiciones y precios pueden modificarse con el tiempo.

---

## 32. Relación con el artículo

Este documento amplía la evidencia técnica presentada en el manuscrito sin modificar su alcance.

El artículo presenta:

- resultados del experimento;
- consumo observado;
- reducciones de procesamiento;
- proyección de almacenamiento;
- delimitación económica.

El repositorio conserva los detalles necesarios para reproducir estos cálculos.

---

## 33. Repositorio

```text
https://github.com/javier1982/retail-cloud-analytics-architecture
```

Este documento forma parte del artefacto técnico de reproducibilidad asociado al artículo científico.
