import flet as ft

FORM_URL = ""

def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            ft.Column([
                ft.Column([
                    ft.Container(
                        content = ft.Text("ストスト🎧レコメンダー", size=50),
                        alignment = ft.alignment.center,
                    ),
                    ft.Container(
                        content = ft.Text("サブスクで聴けるSixTONES楽曲66曲からあなたへおすすめの曲をレコメンド！"),
                        alignment = ft.alignment.center,
                    ),
                    ft.Container(
                        content = ft.Text("注意事項", size=30, color=ft.Colors.WHITE),
                        alignment = ft.alignment.center,
                        bgcolor = ft.Colors.RED_400
                    ),
                    ft.Container(
                        content = ft.Text("※ 非公式のファンサイトです。\n※ 当サイトが提案する楽曲を必ず気に入ることを保証するものではありません。\n※ アップデートは順次行いますが個人運営のため対応には限度があります。", color=ft.Colors.WHITE),
                        alignment = ft.alignment.center,
                        bgcolor = ft.Colors.GREY
                    ),
                    ft.Container(
                        content = ft.FilledButton(
                            content = ft.Text("Start!", size=50),
                            on_click = page.go('question/1'),
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
                        content = ft.Text("ご意見・ご要望はこちらのフォームから", color=ft.Colors.BLUE_400),
                        url = FORM_URL,
                        style = ft.ButtonStyle(
                            bgcolor = ft.Colors.BLUE_100
                        )
                    ),
                    alignment = ft.alignment.center
                )
                ],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            expand=True,
        )
    )


ft.app(main)
