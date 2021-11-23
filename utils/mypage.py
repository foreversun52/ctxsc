class Pagination(object):
    def __init__(self, current_page, all_count, per_page_num=10, pager_count=5):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数

        用法:
        queryset = model.objects.all()
        page_obj = Pagination(current_page,all_count)
        page_data = queryset[page_obj.start:page_obj.end]
        获取数据用page_data而不再使用原始的queryset
        获取前端分页样式用page_obj.page_html
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
                         <div class="layui-card-body ">
                        <div class="page">
                        <div>
                ''')
        first_page = '<a class="prev" href="?page=%s">首页</a>' % (1)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<a class="prev" href ="javascript:return false;" style="opacity: 0.2">上一页</a>'
        else:
            prev_page = '<a class="prev" href="?page=%s">上一页</a>' % (self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = '<span class="current"><a class="num"href="?page=%s">%s</a></span>' % (i, i,)
            else:
                temp = '<a class="num"href="?page=%s">%s</a>' % (i, i,)
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<a class="prev" href ="javascript:return false;" style="opacity: 0.2">下一页</a>'
        else:
            next_page = '<a class="prev" href="?page=%s">下一页</a>' % (self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<a class="prev" href="?page=%s">尾页</a>' % (self.all_pager,)
        page_html_list.append(last_page)
        # 尾部添加标签
        page_html_list.append('''
                                </div>
                            </div>
                        </div>
                                       ''')
        return ''.join(page_html_list)


class IssuePagination(object):
    def __init__(self, current_page, start_date, end_date, data_type, keywords, all_count, per_page_num=10, pager_count=5):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数

        用法:
        queryset = model.objects.all()
        page_obj = Pagination(current_page,all_count)
        page_data = queryset[page_obj.start:page_obj.end]
        获取数据用page_data而不再使用原始的queryset
        获取前端分页样式用page_obj.page_html
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page
        self.start_date = start_date
        self.end_date = end_date
        self.data_type = data_type
        self.keywords = keywords
        self.all_count = all_count
        self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
                         <div class="layui-card-body ">
                        <div class="page">
                        <div>
                ''')
        count_page = f'<font >共计{self.all_count}条</font>&nbsp;&nbsp;&nbsp;&nbsp;'
        page_html_list.append(count_page)
        first_page = f'<a class="prev" href="?page=1&start={self.start_date}&end={self.end_date}&data_type={self.data_type}&keywords={self.keywords}">首页</a>'
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<a class="prev" href ="javascript:return false;" style="opacity: 0.2">上一页</a>'
        else:
            prev_page = f'<a class="prev" href="?page={self.current_page - 1}&start={self.start_date}&end={self.end_date}&data_type={self.data_type}&keywords={self.keywords}">上一页</a>'

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = f'<span class="current"><a class="num"href="?page={i}&start={self.start_date}&end={self.end_date}&data_type={self.data_type}&keywords={self.keywords}">{i}</a></span>'
            else:
                temp = f'<a class="num"href="?page={i}&start={self.start_date}&end={self.end_date}&data_type={self.data_type}&keywords={self.keywords}">{i}</a>'
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<a class="prev" href ="javascript:return false;" style="opacity: 0.2">下一页</a>'
        else:
            next_page = f'<a class="prev" href="?page={self.current_page + 1}&start={self.start_date}&end={self.end_date}&data_type={self.data_type}&keywords={self.keywords}">下一页</a>'
        page_html_list.append(next_page)

        last_page = f'<a class="prev" href="?page={self.all_pager}&start={self.start_date}&end={self.end_date}&data_type={self.data_type}&keywords={self.keywords}">尾页</a>'
        page_html_list.append(last_page)
        # 尾部添加标签
        page_html_list.append('''
                                </div>
                            </div>
                        </div>
                                       ''')
        return ''.join(page_html_list)


class UserPagination(object):
    def __init__(self, current_page, branch_id, all_count, per_page_num=10, pager_count=5):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param pager_count:  最多显示的页码个数

        用法:
        queryset = model.objects.all()
        page_obj = Pagination(current_page,all_count)
        page_data = queryset[page_obj.start:page_obj.end]
        获取数据用page_data而不再使用原始的queryset
        获取前端分页样式用page_obj.page_html
        """
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num
        self.branch_id = branch_id
        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
                         <div class="layui-card-body ">
                        <div class="page">
                        <div>
                ''')
        count_page = f'<font >共计{self.all_count}条</font>&nbsp;&nbsp;&nbsp;&nbsp;'
        page_html_list.append(count_page)
        first_page = f'<a class="prev" href="?page=1&branch_id={self.branch_id}">首页</a>'
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<a class="prev" href ="javascript:return false;" style="opacity: 0.2">上一页</a>'
        else:
            prev_page = f'<a class="prev" href="?page={self.current_page - 1}&branch_id={self.branch_id}">上一页</a>'

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = f'<span class="current"><a class="num"href="?page={i}&branch_id={self.branch_id}">{i}</a></span>'
            else:
                temp = f'<a class="num"href="?page={i}&branch_id={self.branch_id}">{i}</a>'
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<a class="prev" href ="javascript:return false;" style="opacity: 0.2">下一页</a>'
        else:
            next_page = f'<a class="prev" href="?page={self.current_page + 1}&branch_id={self.branch_id}">下一页</a>'
        page_html_list.append(next_page)

        last_page = f'<a class="prev" href="?page={self.all_pager}&branch_id={self.branch_id}">尾页</a>'
        page_html_list.append(last_page)


        # 尾部添加标签
        page_html_list.append('''
                                </div>
                            </div>
                        </div>
                                       ''')
        return ''.join(page_html_list)
