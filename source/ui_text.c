#include "ui_text.h"

/* Compiled into the 3DS binary, so drawing never reads text from the SD card. */
const char *const uiStrings[UI_STRING_COUNT] = {
    [UI_VA_11_HALL_A] = "VA-11 HALL-A",
    [UI_DEN_5_0_8_0] = "ДЕНЬ 5 / 0.26.0",
    [UI_DEN_4_0_8_0] = "ДЕНЬ 4 / 0.26.0",
    [UI_DEN_3_0_8_0] = "ДЕНЬ 3 / 0.26.0",
    [UI_DEN_2_0_8_0] = "ДЕНЬ 2 / 0.26.0",
    [UI_DEN_1_0_8_0] = "ДЕНЬ 1 / 0.26.0",
    [UI_NOVOSTI] = "НОВОСТИ",
    [UI_DZHILL] = "ДЖИЛЛ",
    [UI_EMPTY] = "",
    [UI_APLODISM] = "Аплодисм.",
    [UI_DA_A_A] = "Да-а-а!",
    [UI_BU_U] = "Бу-у!",
    [UI_NET] = "Нет!",
    [UI_HA_HA] = "Ха-ха!",
    [UI_O_O] = "О-о...",
    [UI_CHAT_STRIMA] = "ЧАТ СТРИМА",
    [UI_A] = "A >>",
    [UI_ZAKAZ] = "ЗАКАЗ",
    [UI_NAPITOK_2_2_X_PODAT_OBA] = "Напиток 2/2. X: подать оба",
    [UI_NAPITOK_1_2_X_OTLOZHIT_V_SLOT] = "Напиток 1/2. X: отложить в слот",
    [UI_Y_RETSEPT_A_SHEYKER_X_PODAT] = "Y: рецепт   A: шейкер   X: подать",
    [UI_B_SBROS_L_LD_R_VYDERZHKA] = "B: сброс   L: лёд   R: выдержка",
    [UI_GAME_OVER] = "GAME OVER",
    [UI_DANA_OTPRAVILA_DZHILL_DOMOY] = "Дана отправила Джилл домой.",
    [UI_A_ZAGRUZIT_NACHAT_ZANOVO] = "A: загрузить / начать заново",
    [UI_B_GLAVNOE_MENYU] = "B: главное меню",
    [UI_PERERYV] = "ПЕРЕРЫВ",
    [UI_VREMYA_NEMNOGO_OTDOHNUT] = "Время немного отдохнуть.",
    [UI_A_PRODOLZHIT_SMENU] = "A: продолжить смену",
    [UI_PYATYY_DEN_ZAVERSHN] = "ПЯТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_CHETVRTYY_DEN_ZAVERSHN] = "ЧЕТВЁРТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_TRETIY_DEN_ZAVERSHN] = "ТРЕТИЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_VTOROY_DEN_ZAVERSHN] = "ВТОРОЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_PERVYY_DEN_ZAVERSHN] = "ПЕРВЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_VYRUCHKA] = "Выручка:",
    [UI_CHAEVYE] = "Чаевые:",
    [UI_OSHIBKI] = "Ошибки:",
    [UI_ZARABOTOK] = "Заработок:",
    [UI_A_DOMOY_DEN_5_START_VYHOD] = "A: домой, день 5   START: выход",
    [UI_A_DOMOY_DEN_4_START_VYHOD] = "A: домой, день 4   START: выход",
    [UI_A_DOMOY_DEN_3_START_VYHOD] = "A: домой, день 3   START: выход",
    [UI_A_DOMOY_DEN_2_START_VYHOD] = "A: домой, день 2   START: выход",
    [UI_SELECT_MENYU_START_VYHOD] = "SELECT: меню   START: выход",
    [UI_OSHIBKA_PEREHODA_SELECT_MENYU] = "Ошибка перехода. SELECT: меню",
    [UI_SMENA_OKONCHENA_DOSROCHNO] = "СМЕНА ОКОНЧЕНА ДОСРОЧНО",
    [UI_POSLEDNIY_SEYV_SOHRANN] = "Последний сейв сохранён.",
    [UI_A_ZAGRUZIT_SOHRANENIE] = "A: загрузить сохранение",
    [UI_BEZ_SEYVA_NOVYY_PERVYY_DEN] = "Без сейва: новый первый день.",
    [UI_START_VYHOD] = "START: выход",
    [UI_BAR_OBUCHENIE] = "БАР / ОБУЧЕНИЕ",
    [UI_BAR_DEN_5] = "БАР / ДЕНЬ 5",
    [UI_BAR_DEN_4] = "БАР / ДЕНЬ 4",
    [UI_BAR_DEN_3] = "БАР / ДЕНЬ 3",
    [UI_BAR_DEN_2] = "БАР / ДЕНЬ 2",
    [UI_BAR_DEN_1] = "БАР / ДЕНЬ 1",
    [UI_VZBOLTANO_A_OSTANOVIT] = "Взболтано! A: остановить",
    [UI_SMESHIVAEM_A_OSTANOVIT] = "Смешиваем... A: остановить",
    [UI_NEUDACHNYY_KOKTEYL_B_SBROS] = "Неудачный коктейль: B сброс",
    [UI_DOBAV_INGREDIENTY_Y_RETSEPT] = "Добавь ингредиенты. Y: рецепт",
    [UI_A_CHITAT_DALSHE_Y_RETSEPTY] = "A: читать дальше   Y: рецепты",
    [UI_ADELGID] = "Адельгид",
    [UI_BRONSON_EKSTRAKT] = "Бронсон-экстракт",
    [UI_POROSHKOVAYA_DELTA] = "Порошковая дельта",
    [UI_FLANERGID] = "Фланергид",
    [UI_KARMOTRIN] = "Кармотрин",
    [UI_EMPTY_2] = "-",
    [UI_EMPTY_3] = "+",
    [UI_L_LD_DA] = "L: Лёд [ДА]",
    [UI_L_LD_NET] = "L: Лёд [нет]",
    [UI_R_VYDERZHKA_DA] = "R: Выдержка [ДА]",
    [UI_R_VYDERZHKA] = "R: Выдержка [-]",
    [UI_B_SBROS] = "B: Сброс",
    [UI_A_STOP] = "A: Стоп",
    [UI_A_SHEYKER] = "A: Шейкер",
    [UI_X_PODAT] = "X: Подать",
    [UI_ZVUK_VKLYUCHN] = "Звук: включён",
    [UI_ZVUK_NET_PCM] = "Звук: нет PCM",
    [UI_ZVUK_NET_DSP] = "Звук: нет DSP",
    [UI_OSHIBKA_ZAPISI_SD] = "Ошибка записи SD!",
    [UI_RETSEPTY_L_R] = "РЕЦЕПТЫ   < L / R >",
    [UI_GOTOVYY_NAPITOK_IZ_BUTYLKI] = "Готовый напиток из бутылки.",
    [UI_SHEYKER_NE_NUZHEN] = "Шейкер не нужен.",
    [UI_POKA_NEDOSTUPNO] = "Пока недоступно.",
    [UI_A_NALIT_X_ZATEM_PODAT] = "A: налить   X: затем подать",
    [UI_NALIVAT_MOZHNO_PRI_ZAKAZE] = "Наливать можно при заказе.",
    [UI_DOSTUPEN_BEZ_POKUPKI_V_BETE] = "Доступен без покупки в бете.",
    [UI_KLASSICHESKIY_S_ALKOGOLEM] = "Классический, с алкоголем.",
    [UI_DOSTUPNOST_ZAVISIT_OT_STELLY] = "Доступность зависит от Стеллы.",
    [UI_PO_VKUSU] = "по вкусу",
    [UI_LD_DA] = "Лёд: да",
    [UI_LD_NET] = "Лёд: нет",
    [UI_VYDERZHKA_DA] = "Выдержка: да",
    [UI_VYDERZHKA_NET] = "Выдержка: нет",
    [UI_VZBOLTAT_5_SEKUND_I_DOLSHE] = "Взболтать: 5 секунд и дольше.",
    [UI_SMESHAT_MENEE_5_SEKUND] = "Смешать: менее 5 секунд.",
    [UI_UZHE_BOLSHOY_MAKSIMUM_20_CHASTEY] = "Уже большой. Максимум 20 частей.",
    [UI_BOLSHOY_UDVOY_MAKSIMUM_20] = "Большой: удвой. Максимум 20.",
    [UI_SLADKIY] = "Сладкий",
    [UI_GORKIY] = "Горький",
    [UI_OSTRYY] = "Острый",
    [UI_GAZOVYY] = "Газовый",
    [UI_KISLYY] = "Кислый",
    [UI_IZYSKANNYY] = "Изысканный",
    [UI_ZHENSTVENNYY] = "Женственный",
    [UI_MUZHESTVENNYY] = "Мужественный",
    [UI_REKLAMNYY_PROMO] = "Рекламный (Promo)",
    [UI_KLASSICHESKIY] = "Классический",
    [UI_Y_B_ZAKRYT_L_R_LISTAT] = "Y / B: закрыть   L/R: листать",
    [UI_PAUZA] = "ПАУЗА",
    [UI_A_GLAVNOE_MENYU] = "A: главное меню",
    [UI_A_SOHRANIT_I_OTKRYT_MENYU] = "A: сохранить и открыть меню",
    [UI_B_VERNUTSYA_K_IGRE] = "B: вернуться к игре",
    [UI_X_VYBRAT_MUZYKU] = "X: выбрать музыку",
    [UI_MAGAZIN_UKRASHENIYA_DLYA_DOMA] = "МАГАЗИН / ТОВАРЫ И МУЗЫКА",
    [UI_TREK_NUZHNO_KUPIT] = "Трек продаётся в магазине",
    [UI_KOSHELK] = "Кошелёк:",
    [UI_TSENA] = "Цена:",
    [UI_KUPIT_A_DA_B_OTMENA] = "Купить? A: да / B: отмена",
    [UI_KUPLENO_SOHRANIS_DOMA] = "Куплено. Сохранись дома.",
    [UI_NEDOSTATOCHNO_DENEG] = "Недостаточно денег.",
    [UI_UZHE_KUPLENO] = "Уже куплено.",
    [UI_A_KASANIE_VYBRAT_POKUPKU] = "A / касание: выбрать покупку",
    [UI_B_DOMOY_STRANITSA] = "B: домой  </>: страница",
    [UI_MUZYKALNYY_AVTOMAT] = "МУЗЫКАЛЬНЫЙ АВТОМАТ",
    [UI_VYBERI_MUZYKU_PERED_SMENOY] = "Выбери музыку перед сменой.",
    [UI_MUZYKA_DLYA_ETOY_SMENY] = "Музыка для этой смены",
    [UI_SEYCHAS_VYBRANO] = "Сейчас выбрано:",
    [UI_VYBRANNYY_TREK_IGRAET_PO_KRUGU] = "Выбранный трек играет по кругу.",
    [UI_VVERH_VNIZ_TREK_STRANITSA] = "ВВЕРХ/ВНИЗ: трек  </>: страница",
    [UI_A_KASANIE_IGRAT] = "A / касание: играть",
    [UI_B_OSTAVIT_TEKUSCHIY_TREK] = "B: оставить текущий трек",
    [UI_VA_11_HALL_A_3DS] = "VA-11 HALL-A / 3DS",
    [UI_ORIGINAL_GAME_DEVELOPED_BY] = "Original game developed by",
    [UI_SUKEBAN_GAMES] = "Sukeban Games",
    [UI_MUSIC_BY_GAROAD] = "Music by Garoad",
    [UI_PUBLISHED_BY_YSBRYD_GAMES] = "Published by Ysbryd Games",
    [UI_UNOFFICIAL_FAN_MADE_PORT] = "Unofficial fan-made port",
    [UI_BUILD_WITH_NEUMIRAIE] = "build with neumiraie",
    [UI_NOT_AFFILIATED_WITH_OR_ENDORSED] = "Not affiliated with or endorsed",
    [UI_BY_THE_ORIGINAL_CREATORS] = "by the original creators.",
    [UI_A_TOUCH_CONTINUE] = "A / touch: continue",
    [UI_RUSSKIY_PEREVOD] = "РУССКИЙ ПЕРЕВОД",
    [UI_V_PORTE_ISPOLZUETSYA] = "В порте используется",
    [UI_NEOFITSIALNYY_RUSSKIY_PEREVOD] = "неофициальный русский перевод.",
    [UI_ISTOCHNIK_PEREVODA] = "Источник перевода:",
    [UI_HTTPS_KOSHK_SBS] = "https://koshk.sbs/",
    [UI_SPASIBO_KOMANDE_PEREVODA] = "Спасибо команде перевода!",
    [UI_PEREVOD_SOZDAN_FANATAMI] = "Перевод создан фанатами",
    [UI_I_NE_YAVLYAETSYA_OFITSIALNOY] = "и не является официальной",
    [UI_LOKALIZATSIEY_SUKEBAN_GAMES] = "локализацией Sukeban Games.",
    [UI_A_KASANIE_GLAVNOE_MENYU] = "A / касание: главное меню",
    [UI_VA_11_HALL_A_NINTENDO_3DS] = "VA-11 HALL-A / NINTENDO 3DS",
    [UI_TEST_DNI_1_5_KOSHELK_20000] = "ТЕСТ: дни 1-19 / кошелёк $20000",
    [UI_OTDELNOE_TESTOVOE_SOHRANENIE] = "Отдельное тестовое сохранение",
    [UI_KVARTIRA_DZHILL_DEN_5] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 5",
    [UI_KVARTIRA_DZHILL_DEN_4] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 4",
    [UI_KVARTIRA_DZHILL_DEN_3] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 3",
    [UI_KVARTIRA_DZHILL_DEN_2] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 2",
    [UI_KVARTIRA_DZHILL_DEN_1] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 1",
    [UI_DOPOLNENNAYA_PRAVDA] = "ДОПОЛНЕННАЯ ПРАВДА",
    [UI_DANGER_U] = "DANGER/U/",
    [UI_BLOG_KIRY_MIKI] = "БЛОГ КИРЫ МИКИ",
    [UI_VVERH] = "ВВЕРХ",
    [UI_VNIZ] = "ВНИЗ",
    [UI_B_NAZAD_VVERH_VNIZ_LISTAT] = "B: назад   вверх/вниз: листать",
    [UI_UPRAVLENIE] = "УПРАВЛЕНИЕ",
    [UI_A_DIALOG_SHEYKER_NX_PODAT_B_SBROS_NY_RETSEPTY_L_R_LD] = "A: диалог / шейкер\nX: подать   B: сброс\nY: рецепты   L/R: лёд/выдержка\nКрестовина: ингредиенты\nSELECT: пауза и главное меню\nSTART: сохранить и выйти",
    [UI_SMESHAT_MENEE_5_SEKUND_NVZBOLTAT_OT_5_SEKUND_NAVTOSE] = "Смешать: менее 5 секунд.\nВзболтать: от 5 секунд.\nАвтосейв: в конце дня.",
    [UI_A_B_NAZAD] = "A / B: назад",
    [UI_VA_11_HALL_A_3DS_0_8_0] = "VA-11 HALL-A / 3DS 0.26.0",
    [UI_PRODOLZHIT] = "Продолжить",
    [UI_PRODOLZHIT_NET_SOHRANENIYA] = "Продолжить (нет сохранения)",
    [UI_NOVAYA_IGRA] = "Новая игра",
    [UI_UPRAVLENIE_2] = "Управление",
    [UI_VYHOD] = "Выход",
    [UI_VA_11_HALL_A_0_8_0_TEST] = "VA-11 HALL-A / 0.26.0 TEST",
    [UI_TEST_VYBRAT_DEN] = "Тест: выбрать день",
    [UI_TEST_KVARTIRA_PERED_SMENOY] = "ТЕСТ: ВЫБРАТЬ ДЕНЬ",
    [UI_DEN_1] = "День 1",
    [UI_DEN_2] = "День 2",
    [UI_DEN_3] = "День 3",
    [UI_DEN_4] = "День 4",
    [UI_DEN_5] = "День 5",
    [UI_NOVAYA_IGRA_2] = "НОВАЯ ИГРА",
    [UI_S_OBUCHENIEM] = "С обучением",
    [UI_SRAZU_PERVYY_DEN] = "Сразу первый день",
    [UI_OTMENA] = "Отмена",
    [UI_DOM_17_DEKABRYA] = "ДОМ / 17 ДЕКАБРЯ",
    [UI_DOM_16_DEKABRYA] = "ДОМ / 16 ДЕКАБРЯ",
    [UI_DOM_15_DEKABRYA] = "ДОМ / 15 ДЕКАБРЯ",
    [UI_DOM_14_DEKABRYA] = "ДОМ / 14 ДЕКАБРЯ",
    [UI_DOM_13_DEKABRYA] = "ДОМ / 13 ДЕКАБРЯ",
    [UI_TELEFON] = "Телефон",
    [UI_NA_RABOTU] = "На работу",
    [UI_SOHRANIT] = "Сохранить",
    [UI_MAGAZIN] = "Магазин",
    [UI_TELEFON_2] = "ТЕЛЕФОН",
    [UI_DOPOLNENNAYA_PRAVDA_2] = "Дополненная правда",
    [UI_DANGER_U_2] = "danger/u/",
    [UI_BLOG_KIRY_MIKI_2] = "Блог Киры Мики",
    [UI_MASSOVAYA_EMIGRATSIYA] = "Массовая эмиграция",
    [UI_NOVAYA_UGROZA_VANDERLENDERY] = "Новая угроза: вандерлендеры",
    [UI_KIBORG_NA_KABLUKAH] = "Киборг на каблуках",
    [UI_KONTSERT_MIKI] = "Концерт Мики",
    [UI_POGOVORIM_OB_ALICE_RABBIT] = "Поговорим об Alice_Rabbit",
    [UI_KONTSERT_MIKI_2] = "Концерт Мики 2",
    [UI_KAK_YA_OTDYHAYU] = "Как я отдыхаю",
    [UI_KONTSERT_POD_KUPOLOM] = "Концерт под куполом!",
    [UI_SPASIBO_GLITCH_SITI] = "Спасибо, Глитч-Сити!",
    [UI_KIRA_MIKI] = "КИРА МИКИ",
    [UI_NOVOSTI_16_DEKABRYA] = "Новости / 16 декабря",
    [UI_VTORAYA_STATYA] = "Вторая статья",
    [UI_TRETYA_STATYA] = "Третья статья",
    [UI_NOVOSTI_15_DEKABRYA] = "Новости / 15 декабря",
    [UI_MESTNAYA_GEROINYA] = "Местная героиня",
    [UI_70_NASHIH_CHITATELEY] = "70% наших читателей...",
    [UI_BESPORYADKI_USILIVAYUTSYA] = "Беспорядки усиливаются",
    [UI_KEM_MOZHET_BYT_ALICE_RABBIT] = "Кем может быть Alice_Rabbit?",
    [UI_LECHENIE_TOKIYSKOGO_GRIPPA] = "Лечение токийского гриппа",
    [UI_NOVOSTI_17_DEKABRYA] = "Новости / 17 декабря",
    [UI_TEKUSCHIY_PROGRESS_BUDET_ZAMENN] = "Текущий прогресс будет заменён.",
    [UI_SOHRANENIE_OTPRAVLENO_NA_SD] = "Сохранение отправлено на SD.",
    [UI_A_VYBRAT_B_NAZAD] = "A: выбрать   B: назад",
    [UI_DAY6_BADGE] = "ДЕНЬ 6 / 0.26.0",
    [UI_DAY6_COMPLETED] = "ВЫХОДНОЙ ЗАВЕРШЁН",
    [UI_DAY6_NEXT] = "A: домой, день 6   START: выход",
    [UI_DAY6_SCENE] = "ДОМ / ВЫХОДНОЙ",
    [UI_DAY6_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 6",
    [UI_DAY6_DATE] = "ДОМ / 18 ДЕКАБРЯ",
    [UI_DAY6_BEER_LABEL] = "Выпито банок:",
    [UI_DAY6_DRINK_HINT] = "Y: выпить пиво (до 12)",
    [UI_DAY6_DIALOGUE_HINT] = "A: дальше   Y: пиво",
    [UI_DAY6_NO_SHIFT] = "Сегодня бар был закрыт.",
    [UI_DAY6_FINISH_HINT] = "SELECT: меню   START: выход",
    [UI_DAY6_TEST_LABEL] = "День 6",
    [UI_DAY6_NEWS_TITLE] = "Новости / 18 декабря",
    [UI_DAY7_BADGE] = "ДЕНЬ 7 / 0.26.0",
    [UI_DAY7_COMPLETED] = "СЕДЬМОЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY7_NEXT] = "A: домой, день 7   START: выход",
    [UI_DAY7_FINISH_HINT] = "SELECT: меню   START: выход",
    [UI_DAY7_SCENE] = "БАР / ДЕНЬ 7",
    [UI_DAY7_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 7",
    [UI_DAY7_DATE] = "ДОМ / 19 ДЕКАБРЯ",
    [UI_DAY7_TEST_LABEL] = "День 7",
    [UI_DAY7_NEWS_TITLE] = "Новости / 19 декабря",
    [UI_FOCUS_READY] = "Джилл спокойна перед сменой",
    [UI_DAY2_FOCUS_NEED] = "Джилл отвлекается: нужно голорастение",
    [UI_DAY3_FOCUS_NEED] = "Джилл отвлекается: нужна песня Мики",
    [UI_DAY4_FOCUS_PAID] = "Подписка оплачена: $800",
    [UI_DAY4_FOCUS_MISSED] = "Не хватило $800 на подписку",
    [UI_DAY5_FOCUS_NEED] = "Джилл отвлекается: нужен вентилятор",
    [UI_DAY7_FOCUS_NEED] = "Джилл отвлекается: нужна дарума",
    [UI_DAY8_BADGE] = "ДЕНЬ 8 / 0.26.0",
    [UI_DAY8_COMPLETED] = "ВОСЬМОЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY8_NEXT] = "SELECT: меню   START: выход",
    [UI_DAY8_SCENE] = "БАР / ДЕНЬ 8",
    [UI_DAY8_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 8",
    [UI_DAY8_DATE] = "ДОМ / 20 ДЕКАБРЯ",
    [UI_DAY8_TEST_LABEL] = "День 8",
    [UI_DAY8_NEWS_TITLE] = "Новости / 20 декабря",
    [UI_DAY8_FOCUS_NEED] = "Джилл отвлекается: нужен массажёр",
    [UI_DAY9_BADGE] = "ДЕНЬ 9 / 0.26.0",
    [UI_DAY9_COMPLETED] = "ДЕВЯТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY9_NEXT] = "SELECT: меню   START: выход",
    [UI_DAY9_SCENE] = "БАР / ДЕНЬ 9",
    [UI_DAY9_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 9",
    [UI_DAY9_DATE] = "ДОМ / 21 ДЕКАБРЯ",
    [UI_DAY9_TEST_LABEL] = "День 9",
    [UI_DAY9_NEWS_TITLE] = "Новости / 21 декабря",
    [UI_DAY9_FOCUS_NEED] = "Джилл отвлекается: нужна скидка на пиво",
    [UI_DAY10_BADGE] = "ДЕНЬ 10 / 0.26.0",
    [UI_DAY10_COMPLETED] = "ДЕСЯТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY10_NEXT] = "A: домой / день 11   START: выход",
    [UI_DAY10_SCENE] = "БАР / ДЕНЬ 10",
    [UI_DAY10_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 10",
    [UI_DAY10_DATE] = "ДОМ / 22 ДЕКАБРЯ",
    [UI_DAY10_TEST_LABEL] = "День 10",
    [UI_DAY10_NEWS_TITLE] = "Новости / 22 декабря",
    [UI_DAY10_FOCUS_NEED] = "Джилл отвлекается: нужен постер",
    [UI_DAY11_BADGE] = "ДЕНЬ 11 / 0.26.0",
    [UI_DAY11_COMPLETED] = "ОДИННАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY11_NEXT] = "A: домой / день 12   START: выход",
    [UI_DAY11_SCENE] = "БАР / ДЕНЬ 11",
    [UI_DAY11_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 11",
    [UI_DAY11_DATE] = "ДОМ / 23 ДЕКАБРЯ",
    [UI_DAY11_TEST_LABEL] = "День 11",
    [UI_DAY11_NEWS_TITLE] = "Новости / 23 декабря",
    [UI_DAY11_FOCUS_NEED] = "Джилл отвлекается: нужна ёлка",
    [UI_DAY12_BADGE] = "ДЕНЬ 12 / 0.26.0",
    [UI_DAY12_COMPLETED] = "ДВЕНАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY12_NEXT] = "A: домой / день 13   START: выход",
    [UI_DAY12_SCENE] = "БАР / ДЕНЬ 12",
    [UI_DAY12_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 12",
    [UI_DAY12_DATE] = "ДОМ / 24 ДЕКАБРЯ",
    [UI_DAY12_TEST_LABEL] = "День 12",
    [UI_DAY12_NEWS_TITLE] = "Новости / 24 декабря",
    [UI_DAY12_FOCUS_NEED] = "Джилл отвлекается: не оплачен свет",
    [UI_PARTY_CHOOSE] = "ВЫБЕРИ СОБЕСЕДНИКА",
    [UI_PARTY_QUESTION] = "Правда или действие?",
    [UI_PARTY_GUEST] = "Вечеринка / выбери гостя",
    [UI_PARTY_DANA] = "Дана",
    [UI_PARTY_DOROTHY] = "Дороти",
    [UI_PARTY_RAD] = "Чёткий Сиба",
    [UI_PARTY_ALMA] = "Альма",
    [UI_PARTY_GIL] = "Джиллиан",
    [UI_PARTY_CONTROLS] = "ВВЕРХ/ВНИЗ: выбор   A: говорить",
    [UI_DAY13_BADGE] = "ДЕНЬ 13 / 0.26.0",
    [UI_DAY13_COMPLETED] = "ТРИНАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY13_NEXT] = "A: домой / день 14   START: выход",
    [UI_DAY13_SCENE] = "ВЕЧЕРИНКА / ДЕНЬ 13",
    [UI_DAY13_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 13",
    [UI_DAY13_DATE] = "ДОМ / 25 ДЕКАБРЯ",
    [UI_DAY13_TEST_LABEL] = "День 13",
    [UI_DAY13_NEWS_TITLE] = "Новости / 25 декабря",
    [UI_DAY14_BADGE] = "ДЕНЬ 14 / 0.26.0",
    [UI_DAY14_COMPLETED] = "ЧЕТЫРНАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY14_NEXT] = "A: домой / день 15   START: выход",
    [UI_DAY14_SCENE] = "БАР / ДЕНЬ 14",
    [UI_DAY14_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 14",
    [UI_DAY14_DATE] = "ДОМ / 26 ДЕКАБРЯ",
    [UI_DAY14_TEST_LABEL] = "День 14",
    [UI_DAY14_NEWS_TITLE] = "Новости / 26 декабря",
    [UI_DAY14_FOCUS_NEED] = "Джилл отвлекается: нужна Y2K игра",
    [UI_DAY15_BADGE] = "ДЕНЬ 15 / 0.26.0",
    [UI_DAY15_COMPLETED] = "ПЯТНАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY15_NEXT] = "A: домой / день 16   START: выход",
    [UI_DAY15_SCENE] = "БАР / ДЕНЬ 15",
    [UI_DAY15_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 15",
    [UI_DAY15_DATE] = "ДОМ / 27 ДЕКАБРЯ",
    [UI_DAY15_TEST_LABEL] = "День 15",
    [UI_DAY15_NEWS_TITLE] = "Новости / 27 декабря",
    [UI_DAY15_FOCUS_NEED] = "Джилл отвлекается: нужен Snatcher",
    [UI_DAY16_BADGE] = "ДЕНЬ 16 / 0.26.0",
    [UI_DAY16_COMPLETED] = "ШЕСТНАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY16_NEXT] = "A: домой / день 17   START: выход",
    [UI_DAY16_SCENE] = "БАР / ДЕНЬ 16",
    [UI_DAY16_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 16",
    [UI_DAY16_DATE] = "ДОМ / 28 ДЕКАБРЯ",
    [UI_DAY16_TEST_LABEL] = "День 16",
    [UI_DAY16_NEWS_TITLE] = "Новости / 28 декабря",
    [UI_DAY16_FOCUS_NEED] = "Джилл отвлекается: нужен Манэки-нэко",
    [UI_DAY17_BADGE] = "ДЕНЬ 17 / 0.26.0",
    [UI_DAY17_COMPLETED] = "СЕМНАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY17_NEXT] = "A: домой / день 18   START: выход",
    [UI_DAY17_SCENE] = "БАР / ДЕНЬ 17",
    [UI_DAY17_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 17",
    [UI_DAY17_DATE] = "ДОМ / 29 ДЕКАБРЯ",
    [UI_DAY17_TEST_LABEL] = "День 17",
    [UI_DAY17_NEWS_TITLE] = "Новости / 29 декабря",
    [UI_DAY17_FOCUS_NEED] = "Джилл отвлекается: нужен плакат Киры Мики",
    [UI_DAY18_BADGE] = "ДЕНЬ 18 / 0.26.0",
    [UI_DAY18_COMPLETED] = "ВОСЕМНАДЦАТЫЙ ДЕНЬ ЗАВЕРШЁН",
    [UI_DAY18_NEXT] = "SELECT: меню   START: выход",
    [UI_DAY18_SCENE] = "БАР / ДЕНЬ 18",
    [UI_DAY18_APARTMENT] = "КВАРТИРА ДЖИЛЛ / ДЕНЬ 18",
    [UI_DAY18_DATE] = "ДОМ / 30 ДЕКАБРЯ",
    [UI_DAY18_TEST_LABEL] = "День 18",
    [UI_DAY18_NEWS_TITLE] = "Новости / 30 декабря",
    [UI_DAY18_FOCUS_NEED] = "Джилл отвлекается: не оплачена квартира",
    [UI_DAY19_BADGE] = "ДЕНЬ 19 / 0.26.0",
    [UI_DAY19_COMPLETED] = "НОВОГОДНЯЯ ИСТОРИЯ ЗАВЕРШЕНА",
    [UI_DAY19_NEXT] = "A: эпилог   START: выход",
    [UI_DAY19_SCENE] = "БАР / НОВЫЙ ГОД",
    [UI_DAY19_APARTMENT] = "КВАРТИРА ДЖИЛЛ / НОВЫЙ ГОД",
    [UI_DAY19_DATE] = "ДОМ / 31 ДЕКАБРЯ",
    [UI_DAY19_TEST_LABEL] = "День 19",
    [UI_DAY19_NEWS_TITLE] = "Новости / 30 декабря",
    [UI_EPILOGUE_BADGE] = "ЭПИЛОГ / 0.26.0",
    [UI_EPILOGUE_COMPLETED] = "КОНЕЦ ИСТОРИИ",
    [UI_EPILOGUE_NEXT] = "SELECT: меню   START: выход",
    [UI_EPILOGUE_SCENE] = "ЭПИЛОГ",
    [UI_EPILOGUE_APARTMENT] = "ЭПИЛОГ",
    [UI_EPILOGUE_DATE] = "НОВЫЙ ГОД",
    [UI_CREDITS_SCROLL_HINT] = "ТИТРЫ / ВВЕРХ-ВНИЗ: ПРОКРУТКА",
    [UI_CREDITS_CONTINUE] = "A: перейти к эпилогу",
    [UI_EPILOGUE_TEXT_HINT] = "A: читать дальше   SELECT: меню",
    [UI_PLAYLIST_SLOT] = "ПЛЕЙЛИСТ / СЛОТ",
    [UI_PLAYLIST_PICK] = "Л/П: слот   В/Н: трек",
    [UI_PLAYLIST_SAVE] = "A: в слот   X: начать   B: назад",
    [UI_PLAYLIST_TOGGLE] = "Y: плейлист на 12 треков",
};

static const UiStringId dayBadges[]={UI_DEN_1_0_8_0,UI_DEN_2_0_8_0,UI_DEN_3_0_8_0,UI_DEN_4_0_8_0,UI_DEN_5_0_8_0,UI_DAY6_BADGE,UI_DAY7_BADGE,UI_DAY8_BADGE,UI_DAY9_BADGE,UI_DAY10_BADGE,UI_DAY11_BADGE,UI_DAY12_BADGE,UI_DAY13_BADGE,UI_DAY14_BADGE,UI_DAY15_BADGE,UI_DAY16_BADGE,UI_DAY17_BADGE,UI_DAY18_BADGE,UI_DAY19_BADGE,UI_EPILOGUE_BADGE};
static const UiStringId dayCompleted[]={UI_PERVYY_DEN_ZAVERSHN,UI_VTOROY_DEN_ZAVERSHN,UI_TRETIY_DEN_ZAVERSHN,UI_CHETVRTYY_DEN_ZAVERSHN,UI_PYATYY_DEN_ZAVERSHN,UI_DAY6_COMPLETED,UI_DAY7_COMPLETED,UI_DAY8_COMPLETED,UI_DAY9_COMPLETED,UI_DAY10_COMPLETED,UI_DAY11_COMPLETED,UI_DAY12_COMPLETED,UI_DAY13_COMPLETED,UI_DAY14_COMPLETED,UI_DAY15_COMPLETED,UI_DAY16_COMPLETED,UI_DAY17_COMPLETED,UI_DAY18_COMPLETED,UI_DAY19_COMPLETED,UI_EPILOGUE_COMPLETED};
static const UiStringId nextDayHints[]={UI_A_DOMOY_DEN_2_START_VYHOD,UI_A_DOMOY_DEN_3_START_VYHOD,UI_A_DOMOY_DEN_4_START_VYHOD,UI_A_DOMOY_DEN_5_START_VYHOD,UI_DAY6_NEXT,UI_DAY7_NEXT,UI_DAY8_NEXT,UI_DAY9_NEXT,UI_DAY10_NEXT,UI_DAY11_NEXT,UI_DAY12_NEXT,UI_DAY13_NEXT,UI_DAY14_NEXT,UI_DAY15_NEXT,UI_DAY16_NEXT,UI_DAY17_NEXT,UI_DAY18_NEXT,UI_DAY19_NEXT,UI_EPILOGUE_NEXT};
static const UiStringId barHeadings[]={UI_BAR_DEN_1,UI_BAR_DEN_2,UI_BAR_DEN_3,UI_BAR_DEN_4,UI_BAR_DEN_5,UI_DAY6_SCENE,UI_DAY7_SCENE,UI_DAY8_SCENE,UI_DAY9_SCENE,UI_DAY10_SCENE,UI_DAY11_SCENE,UI_DAY12_SCENE,UI_DAY13_SCENE,UI_DAY14_SCENE,UI_DAY15_SCENE,UI_DAY16_SCENE,UI_DAY17_SCENE,UI_DAY18_SCENE,UI_DAY19_SCENE,UI_EPILOGUE_SCENE};
static const UiStringId apartmentHeadings[]={UI_KVARTIRA_DZHILL_DEN_1,UI_KVARTIRA_DZHILL_DEN_2,UI_KVARTIRA_DZHILL_DEN_3,UI_KVARTIRA_DZHILL_DEN_4,UI_KVARTIRA_DZHILL_DEN_5,UI_DAY6_APARTMENT,UI_DAY7_APARTMENT,UI_DAY8_APARTMENT,UI_DAY9_APARTMENT,UI_DAY10_APARTMENT,UI_DAY11_APARTMENT,UI_DAY12_APARTMENT,UI_DAY13_APARTMENT,UI_DAY14_APARTMENT,UI_DAY15_APARTMENT,UI_DAY16_APARTMENT,UI_DAY17_APARTMENT,UI_DAY18_APARTMENT,UI_DAY19_APARTMENT,UI_EPILOGUE_APARTMENT};
static const UiStringId apartmentDates[]={UI_DOM_13_DEKABRYA,UI_DOM_14_DEKABRYA,UI_DOM_15_DEKABRYA,UI_DOM_16_DEKABRYA,UI_DOM_17_DEKABRYA,UI_DAY6_DATE,UI_DAY7_DATE,UI_DAY8_DATE,UI_DAY9_DATE,UI_DAY10_DATE,UI_DAY11_DATE,UI_DAY12_DATE,UI_DAY13_DATE,UI_DAY14_DATE,UI_DAY15_DATE,UI_DAY16_DATE,UI_DAY17_DATE,UI_DAY18_DATE,UI_DAY19_DATE,UI_EPILOGUE_DATE};
static const UiStringId ingredients[]={UI_ADELGID,UI_BRONSON_EKSTRAKT,UI_POROSHKOVAYA_DELTA,UI_FLANERGID,UI_KARMOTRIN};
static const UiStringId chatReactions[]={UI_EMPTY,UI_APLODISM,UI_DA_A_A,UI_BU_U,UI_NET,UI_HA_HA,UI_O_O};
static int day_index(int day){return day>=1 && day<=20?day-1:0;}
const char *ui_day_badge(int day){return uiStrings[dayBadges[day_index(day)]];}
const char *ui_day_completed(int day){return uiStrings[dayCompleted[day_index(day)]];}
const char *ui_next_day_hint(int day){return uiStrings[nextDayHints[day>=1 && day<=20?day-1:19]];}
const char *ui_bar_heading(int day,int tutorial){return tutorial?uiStrings[UI_BAR_OBUCHENIE]:uiStrings[barHeadings[day_index(day)]];}
const char *ui_apartment_heading(int day){return uiStrings[apartmentHeadings[day_index(day)]];}
const char *ui_apartment_date(int day){return uiStrings[apartmentDates[day_index(day)]];}
const char *ui_ingredient_name(int ingredient){return uiStrings[ingredients[ingredient>=0 && ingredient<5?ingredient:0]];}
const char *ui_chat_reaction(int reaction){return uiStrings[chatReactions[reaction>=0 && reaction<7?reaction:0]];}
const char *ui_phone_forum_title(int entry){
    static const char *const titles[]={"", "Концерт Мики", "Обсудим Alice_Rabbit", "Концерт Мики 2",
        "Концерт Мики 3", "Концерт Мики 4", "Alice_Rabbit: тема 2", "Alice_Rabbit: тема 3",
        "Нападение на банк Аполлон", "Тема Стримчан", "Меня избил Белый рыцарь",
        "Банк Аполлон: часть 2", "Банк Аполлон: часть 3", "Банк Аполлон: часть 4",
        "Бельё NANOCAMO", "AM TOWNSHIPS 64", "Обновление MAKISE EKDV-186",
        "Девушка-монстр Чирари", "Grand Slam Fighters", "Модель-воин снова в эфире",
        "Новый сезон Yooroo Yooree", "Бар под названием VA-11 HALL-A",
        "Как выжить в Глитч-Сити", "Спасибо", "Тема Стримчан"};
    return titles[entry>=1 && entry<=24?entry:1];
}
const char *ui_phone_miki_title(int entry){
    static const char *const titles[]={"", "Как я отдыхаю", "Концерт под куполом", "Спасибо, Глитч-Сити!",
        "Человек мечты", "Мегарождество уже здесь!", "VA-11 HALL-A"};
    return titles[entry>=1 && entry<=6?entry:1];
}
const char *ui_phone_news_title(int day){
    static const UiStringId titles[]={UI_EMPTY,UI_EMPTY,UI_EMPTY,UI_NOVOSTI_15_DEKABRYA,UI_NOVOSTI_16_DEKABRYA,
        UI_NOVOSTI_17_DEKABRYA,UI_DAY6_NEWS_TITLE,UI_DAY7_NEWS_TITLE,UI_DAY8_NEWS_TITLE,
        UI_DAY9_NEWS_TITLE,UI_DAY10_NEWS_TITLE,UI_DAY11_NEWS_TITLE,UI_DAY12_NEWS_TITLE,
        UI_DAY13_NEWS_TITLE,UI_DAY14_NEWS_TITLE,UI_DAY15_NEWS_TITLE,UI_DAY16_NEWS_TITLE,
        UI_DAY17_NEWS_TITLE,UI_DAY18_NEWS_TITLE,UI_DAY19_NEWS_TITLE};
    return uiStrings[titles[day>=3 && day<=19?day:3]];
}
const char *ui_focus_status(int day,int focused,int day4Download){
    if(day==4)return uiStrings[day4Download==1?UI_DAY4_FOCUS_PAID:UI_DAY4_FOCUS_MISSED];
    if(focused)return uiStrings[UI_FOCUS_READY];
    switch(day){
    case 2:return uiStrings[UI_DAY2_FOCUS_NEED];
    case 3:return uiStrings[UI_DAY3_FOCUS_NEED];
    case 5:return uiStrings[UI_DAY5_FOCUS_NEED];
    case 7:return uiStrings[UI_DAY7_FOCUS_NEED];
    case 8:return uiStrings[UI_DAY8_FOCUS_NEED];
    case 9:return uiStrings[UI_DAY9_FOCUS_NEED];
    case 10:return uiStrings[UI_DAY10_FOCUS_NEED];
    case 11:return uiStrings[UI_DAY11_FOCUS_NEED];
    case 12:return uiStrings[UI_DAY12_FOCUS_NEED];
    case 14:return uiStrings[UI_DAY14_FOCUS_NEED];
    case 15:return uiStrings[UI_DAY15_FOCUS_NEED];
    case 16:return uiStrings[UI_DAY16_FOCUS_NEED];
    case 17:return uiStrings[UI_DAY17_FOCUS_NEED];
    case 18:return uiStrings[UI_DAY18_FOCUS_NEED];
    default:return "";
    }
}

const char *ui_order_hint(int n) {
    if(n>=1040 && n<1400){
        static const char *const wandering[]={
            "Что же сейчас заказали?..",
            "Мысли опять куда-то уплыли",
            "Надо вспомнить слова посетителя",
            "Похоже, я прослушала заказ",
            "Дома всё в порядке?..",
            "Сосредоточься, Джилл",
            "Как же неловко переспросить",
            "В голове крутится музыка",
            "Опять думаю не о работе",
            "Заказ был совсем недавно...",
            "Сначала вспомни, потом смешивай"};
        static const char *const subscription[]={
            "Подписка кончилась не вовремя",
            "Голова занята этой подпиской",
            "Не могу забыть про счёт дома",
            "Сосредоточься на заказе, Джилл"};
        int day=(n-1000)/20,variation=(n-1000)%20;
        if(day==4)return subscription[variation%4];
        return wandering[variation%11];
    }
    switch(n) {
    case 1:return "Сахарный прилив";case 2:return "Взрыв на Луне";
    case 3:case 4:return "Большое пиво";case 5:case 7:return "Пиво";
    case 6:return "Большой горький, без алкоголя";
    case 8:return "Большой Удар по печени";
    case 9:return "Сваебой (или Суплекс)";
    case 10:return "Бон Развязон";
    case 11:return "Маленький сладкий со льдом";
    case 12:return "Изысканный напиток (classy)";
    case 13:case 16:return "Брендини";
    case 14:return "Что-нибудь успокаивающее";
    case 15:return "Пианист / Пианистка";
    case 17:return "Как обычно: пиво";
    case 18:case 23:return "Взрыв на Марсе (Marsblast)";
    case 19:case 26:return "Что-нибудь горькое";
    case 20:return "Пианистка";
    case 21:return "Взрыв на Луне";
    case 22:return "Большой Sunshine Cloud + Gut Punch";
    case 24:return "Похожий на чай: горький, женственный";
    case 25:return "Что-нибудь мягкое";
    case 27:return "Bad Touch";
    case 28:return "Необычный напиток (Promo)";
    case 29:return "Большой Брендини";
    case 30:return "Как обычно: пиво";
    case 31:return "Bleeding Jane";
    case 32:return "Напиток с изменённым названием";
    case 33:return "В честь хорошего друга";
    case 34:return "Два Бон Развязона";
    case 35:return "Две Blue Fairy";
    case 36:return "Напиток за $80";
    case 37:return "Grizzly Temple";
    case 38:return "Мерзкий: Manly или Promo";
    case 39:return "Большой Bad Touch";
    case 40:return "Что-нибудь, чтобы опьянеть";
    case 41:return "Два пива";
    case 42:return "Zen Star";
    case 43:return "Два Брендини";
    case 44:return "Два мужественных (Manly)";
    case 45:return "Взрыв на Марсе";
    case 46:return "Пиво";
    case 47:return "Ром";case 48:return "Blue Fairy";case 49:return "Пиво";
    case 50:return "Cobalt Velvet";case 51:return "Бон Развязон";case 52:return "Абсент";
    case 53:return "Что-нибудь с алкоголем";case 54:return "Брендини";
    case 55:return "Сладкий без алкоголя";case 56:return "Ровно 17 частей ингредиентов";case 57:return "Plumfume";
    case 58:return "Sugar Rush";case 59:return "Suplex или Piledriver";
    case 60:return "Пиво";case 61:return "Zen Star";
    case 62:return "Два Bad Touch";case 63:return "Piano Man";
    case 64:return "Пиво";case 65:return "Взрыв на Марсе";
    case 66:return "Piano Man";case 67:return "Напиток для Вирджилио";
    case 68:return "На усмотрение бармена";
    case 69:return "Что-нибудь сладкое";
    case 70:return "Fluffy Dream";
    case 71:return "Сладкий без алкоголя";
    case 72:return "Bleeding Jane (или сладкий)";
    case 73:return "Удар по печени";
    case 74:return "Горький или мужественный";
    case 75:return "Пиво";
    case 76:return "Bleeding Jane";
    case 77:return "Zen Star";
    case 78:return "Fluffy Dream без алкоголя";
    case 79:return "Marsblast или Piano Woman";
    case 80:return "Gut Punch или Moonblast";
    case 81:return "Fringe Weaver";
    case 82:return "Bleeding Jane";
    case 83:return "Большая Blue Fairy";
    case 84:return "Cobalt Velvet";
    case 178:return "Пиво для Гила";
    case 85:return "Бенгальский огонь";
    case 86:return "Проникновение (Bad Touch)";
    case 87:return "Пиво";
    case 88:return "Что-нибудь со льдом";
    case 89:return "Большой Брендини";
    case 90:return "Два Свечения";
    case 92:return "Два пива";
    case 93:return "Золотое облако";
    case 94:return "Большой игристый напиток";
    case 95:return "Любой напиток";
    case 96:return "Мужественный или горький";
    case 97:return "Пиво";
    case 98:return "Свечение и Бон Развязон";
    case 99:return "Напиток для Альмы";
    case 100:return "Алкогольный напиток";
    case 101:return "Что-нибудь сладкое";
    case 102:return "Напиток для Джилл";
    case 103:return "Пиво для Джилл";
    case 104:return "Брендини";
    case 105:return "Fluffy Dream";
    case 106:return "Напиток для Дороти";
    case 107:return "Blue Fairy";
    case 108:return "Blue Fairy";
    case 109:return "Сладкий со льдом";
    case 110:return "Без алкоголя";
    case 111:return "Мужественный напиток";
    case 112:return "Cobalt Velvet";
    case 113:return "Bleeding Jane";
    case 114:return "Острый напиток";
    case 115:return "Горький напиток";
    case 116:return "Gut Punch";
    case 117:return "Fringe Weaver";
    case 175:return "Fringe Weaver";
    case 176:return "Sugar Rush";
    case 163:return "Пиво";
    case 164:return "Sugar Rush";
    case 165:return "Газированный напиток";
    case 167:return "Напиток для Гэби";
    case 118:return "Cobalt Velvet";
    case 119:return "Сладкий со льдом";
    case 120:return "Два пива";
    case 121:return "Изысканный напиток";
    case 122:return "Газированный напиток";
    case 123:return "Сладкий напиток";
    case 124:return "Любой напиток";
    case 125:case 126:return "Напиток для Марио";
    case 127:return "Piano Man или Piano Woman";
    case 128:return "Marsblast для Инграма";
    case 129:return "Suplex для Инграма";
    case 130:return "Fringe Weaver для Инграма";
    case 131:return "Gut Punch для Инграма";
    case 132:case 133:return "Сладкий напиток для Инграма";
    case 134:return "Bad Touch для Альмы";
    case 135:case 140:return "Брендини";
    case 136:case 138:return "Пиво";
    case 137:return "Bleeding Jane";
    case 139:return "Fluffy Dream";
    case 141:return "Zen Star";
    case 142:return "Обычное пиво для Донована";
    case 143:return "Взрыв на Луне";
    case 144:return "Сваебой";
    case 145:return "Сладкий напиток для Мики";
    case 146:return "Напиток со вкусом чая";
    case 147:return "Sparkle Star";
    case 148:return "Bleeding Jane";
    case 149:case 152:return "Брендини";
    case 150:return "Классический напиток";
    case 151:return "Сахарный прилив";
    case 168:return "Большой Cobalt Velvet";
    case 169:return "Сахарный прилив";
    case 170:return "Пиво";
    case 153:return "Пятничное пиво";
    case 154:return "Bloom Light и безалкогольный напиток";
    case 155:return "Piano Man и Piano Woman";
    case 156:return "Неприятный напиток";
    case 157:return "Женственный напиток";
    case 158:return "Gut Punch";
    case 159:return "Сладкий напиток";
    case 160:case 161:return "Сахарный прилив";
    case 162:return "Два больших пива";
    case 174:return "Пиво или другой алкоголь";
    default:return "Заказ посетителя";
    }
}
