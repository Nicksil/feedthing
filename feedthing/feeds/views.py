import feedparser


# def add_feed(request):
#     url = request.POST.get('url')
#     parsed = feedparser.parse(url)
#     href = parsed['href']
#     title = parsed['feed']['title']
#
#     Feed.objects.create(
#         href=href,
#         title=title,
#         user=request.user
#     )
#
#     return redirect('feeds:index')
