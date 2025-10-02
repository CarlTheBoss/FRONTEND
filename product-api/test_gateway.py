#!/usr/bin/env python3
"""
Script de prueba para el API Gateway
Verifica la conectividad con todas las APIs
"""

import requests
import json
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# URL base del gateway
GATEWAY_URL = "http://localhost:5000"


def print_header(text):
    """Imprime un encabezado formateado"""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")


def print_success(text):
    """Imprime un mensaje de éxito"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_error(text):
    """Imprime un mensaje de error"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


def print_warning(text):
    """Imprime un mensaje de advertencia"""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_info(text):
    """Imprime un mensaje informativo"""
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")


def test_endpoint(name, url, expected_keys=None):
    """
    Prueba un endpoint específico

    Args:
        name: Nombre del endpoint
        url: URL completa del endpoint
        expected_keys: Lista de claves esperadas en la respuesta
    """
    try:
        print(f"\n{Fore.YELLOW}Probando: {name}{Style.RESET_ALL}")
        print(f"URL: {url}")

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print_success(f"Status: {response.status_code}")

            try:
                data = response.json()

                # Mostrar cantidad de elementos si es una lista
                if isinstance(data, list):
                    print_info(f"Elementos recibidos: {len(data)}")
                    if len(data) > 0:
                        print_info(f"Muestra del primer elemento:")
                        print(json.dumps(data[0], indent=2, ensure_ascii=False))
                elif isinstance(data, dict):
                    print_info(f"Objeto recibido con {len(data)} claves")
                    if expected_keys:
                        missing_keys = [key for key in expected_keys if key not in data]
                        if missing_keys:
                            print_warning(f"Claves faltantes: {missing_keys}")
                        else:
                            print_success("Todas las claves esperadas están presentes")
                    print(json.dumps(data, indent=2, ensure_ascii=False))

                return True
            except json.JSONDecodeError:
                print_error("La respuesta no es JSON válido")
                print(f"Respuesta: {response.text[:200]}")
                return False
        else:
            print_error(f"Status: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            return False

    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al endpoint")
        return False
    except requests.exceptions.Timeout:
        print_error("Timeout al conectar con el endpoint")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        return False


def test_post_endpoint(name, url, data):
    """
    Prueba un endpoint POST

    Args:
        name: Nombre del endpoint
        url: URL completa del endpoint
        data: Datos a enviar en el POST
    """
    try:
        print(f"\n{Fore.YELLOW}Probando POST: {name}{Style.RESET_ALL}")
        print(f"URL: {url}")
        print(f"Datos enviados:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        response = requests.post(url, json=data, timeout=10)

        if response.status_code in [200, 201]:
            print_success(f"Status: {response.status_code}")

            try:
                result = response.json()
                print_success("Respuesta:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return True
            except json.JSONDecodeError:
                print_error("La respuesta no es JSON válido")
                return False
        else:
            print_error(f"Status: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            return False

    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    """Función principal de pruebas"""
    print_header("🧪 PRUEBAS DEL API GATEWAY")

    results = []

    # 1. Probar endpoint principal
    print_header("1. Probando Endpoint Principal")
    results.append(
        test_endpoint(
            "Gateway Home", f"{GATEWAY_URL}/", expected_keys=["message", "endpoints"]
        )
    )

    # 2. Probar health check
    print_header("2. Probando Health Check")
    results.append(
        test_endpoint(
            "Health Check", f"{GATEWAY_URL}/health", expected_keys=["gateway", "apis"]
        )
    )

    # 3. Probar endpoint de categorías
    print_header("3. Probando Endpoint de Categorías")
    results.append(
        test_endpoint("Categorías (Python API)", f"{GATEWAY_URL}/categorias")
    )

    # 4. Probar endpoint de marcas
    print_header("4. Probando Endpoint de Marcas")
    results.append(test_endpoint("Marcas (Node.js API)", f"{GATEWAY_URL}/marcas"))

    # 5. Probar endpoint de unidades
    print_header("5. Probando Endpoint de Unidades")
    results.append(test_endpoint("Unidades (PHP API)", f"{GATEWAY_URL}/unidades"))

    # 6. Probar endpoint de productos
    print_header("6. Probando Endpoint de Productos")
    results.append(test_endpoint("Productos (Java API)", f"{GATEWAY_URL}/productos"))

    # 7. Probar endpoint de todos los datos
    print_header("7. Probando Endpoint ALL (Todos los Datos)")
    results.append(
        test_endpoint(
            "Todos los Datos",
            f"{GATEWAY_URL}/all",
            expected_keys=["categorias", "marcas", "unidades", "productos", "errors"],
        )
    )

    # 8. Probar creación de producto (opcional)
    print_header("8. Probando Creación de Producto (POST)")
    test_product = {
        "nom_pro": "Producto de Prueba",
        "pre_pro": 99.99,
        "id_uni": 1,
        "id_marca": 1,
        "id_cat": 1,
        "stk_pro": 10.0,
        "estado": "Y",
    }
    print_warning(
        "Esta prueba puede fallar si el backend no acepta POST o requiere autenticación"
    )
    # results.append(test_post_endpoint(
    #     "Crear Producto",
    #     f"{GATEWAY_URL}/productos",
    #     test_product
    # ))

    # Resumen de resultados
    print_header("📊 RESUMEN DE PRUEBAS")

    total_tests = len(results)
    passed_tests = sum(results)
    failed_tests = total_tests - passed_tests

    print(f"\n{Fore.CYAN}Total de pruebas: {total_tests}")
    print(f"{Fore.GREEN}Pruebas exitosas: {passed_tests}")
    print(f"{Fore.RED}Pruebas fallidas: {failed_tests}")

    if passed_tests == total_tests:
        print(f"\n{Fore.GREEN}{'=' * 60}")
        print(f"{Fore.GREEN}✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print(f"{Fore.GREEN}{'=' * 60}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}{'=' * 60}")
        print(f"{Fore.YELLOW}⚠ ALGUNAS PRUEBAS FALLARON")
        print(f"{Fore.YELLOW}Verifica que todas las APIs backend estén corriendo")
        print(f"{Fore.YELLOW}{'=' * 60}{Style.RESET_ALL}")

    # Información adicional
    print(f"\n{Fore.BLUE}{'=' * 60}")
    print(f"{Fore.BLUE}ℹ INFORMACIÓN ADICIONAL")
    print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    print("\nAPIs que deben estar corriendo:")
    print(f"  • Python (Categorías): http://localhost:3001/")
    print(f"  • Node.js (Marcas): http://localhost:3002/")
    print(f"  • PHP (Unidades): http://localhost:3003/")
    print(f"  • Java (Productos): URL externa configurada")
    print(f"\nGateway:")
    print(f"  • Flask Gateway: {GATEWAY_URL}")

    print(f"\n{Fore.CYAN}Para ver los logs del gateway:")
    print(f"{Fore.CYAN}  tail -f logs/gateway.log{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Pruebas interrumpidas por el usuario{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error fatal: {str(e)}{Style.RESET_ALL}")
