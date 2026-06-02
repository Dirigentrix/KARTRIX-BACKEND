# Szybkie podsumowanie

KARTRIX-BACKEND ma zamknąć sprint wokół jednego spójnego celu: doprowadzić rdzeń DARTRIX/KARTRIX do stanu demonstracyjnego, z jasnym podziałem ról agentów, zweryfikowaną strategią COMFESSI, gotowymi scenariuszami demo i checklistą techniczną do 11 czerwca.

Priorytety sprintu:
- domknięcie architektury agentów
- dopięcie walidacji COMFESSI
- przygotowanie ścieżek demo
- uporządkowanie dokumentacji i checklisty wdrożeniowej

# Agent map

## 1. Orchestrator / Planner
Rola: sterowanie kolejnością zadań, pilnowanie zależności i synchronizacja sprintu.

Zakres:
- rozbijanie zadań na kroki
- nadzorowanie statusu blokad
- pilnowanie granicy 11 czerwca

## 2. KARTRIX Core
Rola: główny silnik logiki systemu.

Zakres:
- logika rdzenia
- przygotowanie kontraktów wejścia i wyjścia
- spójność z manifestem DARTRIX

## 3. Shadow Interface
Rola: warstwa wizualna i interakcyjna.

Zakres:
- ekran/powłoka demonstracyjna
- czytelne stany systemu
- wizualizacja aktywacji i przepływu

## 4. COMFESSI Verifier
Rola: walidacja jakości i gotowości komunikacyjnej.

Zakres:
- cohesion
- correspondence
- pragmatism
- wynik walidacji jako sygnał gotowości do kolejnego kroku

## 5. Demo Runner
Rola: uruchomienie scenariuszy pokazowych i weryfikacja przebiegu.

Zakres:
- scenariusze demo
- kontrola stanów
- test przejść między etapami

# COMFESSI strategy

COMFESSI ma być prostą warstwą oceny spójności sprintu:

- Cohesion: czy wszystkie elementy planu prowadzą do jednego celu
- Correspondence: czy dokumentacja, implementacja i demo są zgodne
- Pragmatism: czy zakres da się dowieźć w czasie sprintu

Zasada operacyjna:
- każdy element sprintu musi dać się obronić w trzech wymiarach COMFESSI
- jeśli którykolwiek wymiar jest słaby, zadanie wraca do doprecyzowania

# Demo scenarios

## Scenariusz 1: Activation path
- wejście do systemu
- uruchomienie rdzenia
- pokazanie przejścia od sygnału do struktury
- zakończenie stanem gotowości

## Scenariusz 2: Agent coordination
- pokazanie mapy agentów
- pokazanie, kto odpowiada za plan, rdzeń, walidację i demo
- demonstracja kolejności wywołań

## Scenariusz 3: COMFESSI validation
- podanie krótkiego opisu sprintu
- walidacja spójności, zgodności i pragmatyzmu
- prezentacja wyniku i decyzji o dalszym kroku

## Scenariusz 4: Delivery checkpoint
- sprawdzenie checklisty technicznej
- potwierdzenie, że demo i dokumentacja są gotowe
- zamknięcie sprintu przed 11 czerwca

# Technical checklist until June 11

## June 2
- utworzyć plik sprint-plan.md
- ustalić finalny zakres sprintu
- potwierdzić mapę agentów

## June 3
- doprecyzować kontrakty między agentami
- sprawdzić spójność z manifestem DARTRIX
- zebrać brakujące zależności

## June 4
- dopiąć COMFESSI verification flow
- upewnić się, że wynik walidacji jest jednoznaczny
- zamknąć pola wejścia i wyjścia

## June 5
- przygotować scenariusz activation path
- przygotować scenariusz agent coordination
- przetestować kolejność kroków

## June 6
- przygotować scenariusz COMFESSI validation
- dopracować komunikaty statusowe
- usunąć niespójności w nazewnictwie

## June 7
- przygotować scenariusz delivery checkpoint
- przegląd dokumentacji technicznej
- zidentyfikować ryzyka dla demo

## June 8
- wdrożyć poprawki po przeglądzie
- sprawdzić stabilność przejść między stanami
- potwierdzić gotowość interfejsu demo

## June 9
- wykonać test end-to-end planu sprintu
- zweryfikować pełną ścieżkę od wejścia do demo
- zamknąć otwarte zadania

## June 10
- finalny przegląd dokumentacji
- przygotowanie wersji do pokazania
- przygotowanie planu awaryjnego

## June 11
- checkpoint końcowy
- potwierdzenie gotowości demo
- zamknięcie sprintu i zapis statusu

# Notes

This file is the sprint working plan for Dirigentrix/KARTRIX-BACKEND and should stay aligned with the DARTRIX ecosystem documents.
