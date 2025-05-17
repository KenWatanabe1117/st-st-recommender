import flet as ft
from bayesian_recommender import BayesianRecommender

FORM_URL = "https://forms.gle/W3YHvCsGCiEvLshQ7"
CONFIDENCE_THRESHOLD = 0.95

def main(page: ft.Page):
    recommender = BayesianRecommender()
    confidence = recommender.get_best_belief()
    #ホーム画面の見た目の設定
    home_view = ft.View(
        "/",
        [
            ft.AppBar(title = ft.Text("ストスト🎧レコメンダー", size=50),
                      center_title = True,
                      bgcolor = ft.Colors.BLUE_400,
                      toolbar_height = 66),
            ft.SafeArea(
                ft.Column([
                    ft.Column([
                        ft.Container(
                            content = ft.Text("サブスクで聴けるSixTONES楽曲66曲からあなたへおすすめの曲をレコメンド！", size=24),
                            alignment = ft.alignment.center,
                        ),
                        ft.Container(
                            content = ft.Text("注意事項", size=32, color=ft.Colors.WHITE),
                            alignment = ft.alignment.center,
                            bgcolor = ft.Colors.RED_400,
                            padding = 10
                        ),
                        ft.Container(
                            content = ft.Text("※ 非公式のファンサイトです。\n※ 当サイトが提案する楽曲を必ず気に入ることを保証するものではありません。\n※ アップデートは順次行いますが個人運営のため対応には限度があります。", size=24, color=ft.Colors.WHITE),
                            alignment = ft.alignment.center,
                            bgcolor = ft.Colors.GREY,
                            padding = 10
                        ),
                        ft.Container(
                            content = ft.FilledButton(
                                content = ft.Text("Start!", size=50),
                                on_click = lambda _: page.go("/question/1"),
                                style = ft.ButtonStyle(
                                    shape = ft.CircleBorder(),
                                    padding = 50
                                )
                            ),
                            alignment = ft.alignment.center
                        )
                    ]),
                    ft.Container(
                        content = ft.TextButton(
                            content = ft.Text("ご意見・ご要望はこちらのフォームから", size=24, color=ft.Colors.BLUE_400),
                            url = FORM_URL,
                            style = ft.ButtonStyle(
                                bgcolor = ft.Colors.BLUE_100,
                                padding = 10
                            )
                        ),
                        alignment = ft.alignment.center
                    )],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                expand=True,
            )]
    )

    def answer_clicked(question, answer_score, count):
        nonlocal recommender, confidence
        best_id, confidence = recommender.update_belief(question, answer_score)
        if confidence >= CONFIDENCE_THRESHOLD:
            page.go(f"/result/{best_id}")
        else:
            page.go(f"/question/{int(count)+1}")


    def create_question_view(count):
        nonlocal recommender, confidence
        question = recommender.select_best_question()
        return ft.View(
            f"/question/{count}",
            [
                ft.AppBar(title = ft.Text(f"Question {count}", size=50),
                            bgcolor = ft.Colors.BLUE_400,
                            toolbar_height = 66
                ),
                ft.ProgressBar(
                    value = confidence / CONFIDENCE_THRESHOLD,
                    color = ft.Colors.BLUE_200,
                    bar_height = 8
                ),
                ft.Text(f"{question}", size=24),
                ft.ElevatedButton(
                    "好き",
                    color = ft.Colors.RED_400,
                    bgcolor = ft.Colors.RED_100,
                    icon = ft.CupertinoIcons.HEART_FILL,
                    icon_color = ft.Colors.RED_400,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    on_click = lambda _: answer_clicked(question, 1.0, count)
                ),
                ft.ElevatedButton(
                    "どちらかといえば好き",
                    color = ft.Colors.PINK_400,
                    bgcolor = ft.Colors.PINK_100,
                    icon = ft.CupertinoIcons.HEART_FILL,
                    icon_color = ft.Colors.PINK_400,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    on_click = lambda _: answer_clicked(question, 0.5, count)
                ),
                ft.ElevatedButton(
                    "どちらともいえない",
                    color = ft.Colors.AMBER_600,
                    bgcolor = ft.Colors.AMBER_100,
                    icon = ft.CupertinoIcons.HEART_FILL,
                    icon_color = ft.Colors.AMBER_600,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    on_click = lambda _: answer_clicked(question, 0, count)
                ),
                ft.ElevatedButton(
                    "どちらかといえば好きではない",
                    color = ft.Colors.GREEN_400,
                    bgcolor = ft.Colors.GREEN_100,
                    icon = ft.CupertinoIcons.HEART_FILL,
                    icon_color = ft.Colors.GREEN_400,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    on_click = lambda _: answer_clicked(question, -0.5, count)
                ),
                ft.ElevatedButton(
                    "好きではない",
                    color = ft.Colors.BLUE_400,
                    bgcolor = ft.Colors.BLUE_100,
                    icon = ft.CupertinoIcons.HEART_FILL,
                    icon_color = ft.Colors.BLUE_400,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    on_click = lambda _: answer_clicked(question, -1.0, count)
                ),
                ft.ElevatedButton(
                    "わからない",
                    color = ft.Colors.BLACK,
                    bgcolor = ft.Colors.GREY_100,
                    icon = ft.CupertinoIcons.HEART_FILL,
                    icon_color = ft.Colors.BLACK,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    on_click = lambda _: answer_clicked(question, 0, count)
                )
            ]
        )

    def create_result_view(id):
        top_5_ids, song_names, confidences = recommender.recommend_top_k(5)
        top_song_name = song_names[top_5_ids==int(id)][0]
        urls = recommender.get_urls(top_song_name)
        keywords = recommender.get_keywords(top_song_name)
        return ft.View(
            f"/result/{id}",
            [
                ft.AppBar(title = ft.Text(f"あなたへのおすすめの楽曲はこちら！", size=50),
                            bgcolor = ft.Colors.BLUE_400,
                            toolbar_height = 66),
                ft.Text(f"{top_song_name} (おすすめ度 {confidences[top_5_ids==int(id)][0]*100:.2f}%)", size=50),
                ft.Text("キーワード\n" + "、".join(keywords), size=24),
                ft.ElevatedButton(
                    "YouTubeで見る",
                    color = ft.Colors.RED_400,
                    bgcolor = ft.Colors.RED_100,
                    icon = ft.CupertinoIcons.PLAY_RECTANGLE,
                    icon_color = ft.Colors.RED_400,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    url = urls.at[int(id),"YouTube"]
                ),
                ft.ElevatedButton(
                    "Spotifyで聴く",
                    color = ft.Colors.GREEN_400,
                    bgcolor = ft.Colors.GREEN_100,
                    icon = ft.CupertinoIcons.PLAY_CIRCLE,
                    icon_color = ft.Colors.GREEN_400,
                    style = ft.ButtonStyle(
                        text_style = ft.TextStyle(
                            size = 24
                        ),
                        icon_size = 24,
                        padding = 10
                    ),
                    url = urls.at[int(id),"Spotify"]
                ),
                ft.TextButton(
                    content = ft.Text("ホームに戻る", size=24, color=ft.Colors.BLUE_400),
                    on_click = lambda _: page.go("/"),
                    style = ft.ButtonStyle(
                        bgcolor = ft.Colors.BLUE_100,
                        padding = 10
                    )
                )
            ]
        )

    #ルートを変更したときの動作
    def route_change(handler):
        troute = ft.TemplateRoute(handler.route)
        if troute.match("/"):
            page.views.clear()
            page.views.append(home_view)
            recommender.__init__()
        elif troute.match("/question/:count"):
            page.views.append(create_question_view(troute.count))
        elif troute.match("/result/:id"):
            page.views.append(create_result_view(troute.id))
        page.update()

    #戻るときの動作
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.title = "ストストレコメンダー"
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.views.clear()
    page.go(page.route)

ft.app(main, view=ft.AppView.WEB_BROWSER)
